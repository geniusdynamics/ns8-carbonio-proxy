#
# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Helpers of the NS8 Carbonio edge proxy module.

The proxy joins a ns8-carbonio main server (CARBONIO_JOIN). The Carbonio
proxy role (nginx and memcached) finds every mailbox server through the
directory of the main server: no upstream list is written here, new
mailbox servers are routed as soon as they exist in the directory.

Service records (non-secret) of the ns8-carbonio instances, read to list
the main servers and to resolve the host names of the installation:

    module/<module_id>/srv/tcp/carbonio  (hash)
        host, fqdn, role, master, node, release, accept_join, ...

and of this proxy:

    module/<module_id>/srv/tcp/carbonio-proxy  (hash)
        host         WireGuard address of the node
        fqdn         Carbonio server name of the proxy
        role         proxy
        master       module id of the main server
        node         node id
        release      Carbonio release
        public_host  web host name

Secrets never go to Redis in clear: see seal_bundle() / open_bundle().
"""

import base64
import errno
import json
import os
import secrets
import socket
import string
import subprocess
import sys

import agent

SECRETS_FILE = "secrets.env"
CONTAINER = "carbonio"
SERVICE = "carbonio.service"
SRV_NAME = "carbonio-proxy"

# Passwords shared by every server of a Carbonio installation: the LDAP
# accounts of the services. A server that joins receives them from the
# master, sealed (see seal_bundle).
SHARED_SECRETS = [
    "CARBONIO_LDAP_ZIMBRA_PASSWORD",
    "CARBONIO_LDAP_POSTFIX_PASSWORD",
    "CARBONIO_LDAP_AMAVIS_PASSWORD",
    "CARBONIO_LDAP_NGINX_PASSWORD",
    "CARBONIO_LDAP_REPLICATION_PASSWORD",
]
# Local to each server
LOCAL_SECRETS = [
    "CARBONIO_LDAP_ROOT_PASSWORD",
    "CARBONIO_KEYSTORE_PASSWORD",
]

# Public IMAP and POP3 ports of the proxy. SMTP stays on the main server.
MAIL_PORTS = [110, 143, 993, 995]
# Nothing is published on the WireGuard address: the proxy only connects
# to the mailbox servers (since Carbonio 26.3 memcached listens on the
# loopback only, its route cache is not cleared from the mailbox servers)
PROXY_VPN_PORTS = []

# Modules that bind the public mail ports of a node
MAIL_MODULE_IMAGES = {
    "mail", "mailcow", "carbonio", "carbonio-proxy", "postal", "kumomta",
    "stalwart", "mailu", "iredmail", "mailserver", "docker-mailserver",
}



def log(message):
    print(message, file=sys.stderr)


def is_true(value):
    return str(value).lower() in ("1", "true", "yes", "on")


def genpw(length=32):
    """Alphanumeric secret: the values end up in the Carbonio setup
    configuration and in LDAP URLs"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def read_secrets():
    try:
        return agent.read_envfile(SECRETS_FILE)
    except FileNotFoundError:
        return {}


def write_secrets(values):
    """KEY=VALUE lines readable by the module user only (0600)"""
    tmp = f"{SECRETS_FILE}.{os.getpid()}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fenv:
        for key, value in sorted(values.items()):
            fenv.write(f"{key}={value}\n")
    os.replace(tmp, SECRETS_FILE)


def ensure_secrets():
    """Generate the missing secrets once. The admin password is set by the
    administrator in configure-module."""
    current = read_secrets()
    changed = False
    for key in SHARED_SECRETS + LOCAL_SECRETS:
        if not current.get(key):
            current[key] = genpw()
            changed = True
    if changed:
        write_secrets(current)
    return current


def _environment():
    """The module environment file, read again on each call: values set by
    agent.set_env() in a previous step of the same action are not in
    os.environ yet"""
    values = dict(os.environ)
    path = os.path.join(os.environ.get("AGENT_STATE_DIR", "."), "environment")
    try:
        values.update(agent.read_envfile(path))
    except (FileNotFoundError, KeyError):
        pass
    return values


def env(name, default=""):
    value = _environment().get(name)
    return default if value is None or value == "" else value


def cluster_role():
    return "proxy"


def container_role():
    """Role of the Carbonio container (carbonio-run CARBONIO_ROLE)"""
    return "proxy"


def initialized():
    """The first Carbonio setup completed (set by 80start_services)"""
    return env("CARBONIO_INITIALIZED") == "1"


def tcp_ports():
    ports = [p for p in env("TCP_PORTS", env("TCP_PORT", "")).split(",") if p]
    return [int(p) for p in ports]


def get_timezone():
    try:
        target = os.path.realpath("/etc/localtime")
        if "/zoneinfo/" in target:
            return target.split("/zoneinfo/", 1)[1]
    except OSError:
        pass
    return "UTC"


def node_vpn_ip(rdb=None, node_id=None):
    rdb = rdb or agent.redis_connect(use_replica=True)
    return rdb.hget(f"node/{node_id or env('NODE_ID')}/vpn", "ip_address") or ""


def cluster_network(rdb=None):
    rdb = rdb or agent.redis_connect(use_replica=True)
    return rdb.get("cluster/network") or ""


def port_in_use(port):
    """True if a socket listens on the TCP port. SO_REUSEADDR: connections
    in TIME_WAIT (a service that just stopped) are not a listener."""
    for family, addr in ((socket.AF_INET, "0.0.0.0"), (socket.AF_INET6, "::")):
        try:
            sock = socket.socket(family, socket.SOCK_STREAM)
        except OSError:
            continue
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((addr, port))
        except OSError as ex:
            if ex.errno in (errno.EADDRINUSE, errno.EACCES):
                return True
        finally:
            sock.close()
    return False


def image_name_of(rdb, module_id):
    image_url = rdb.hget(f"module/{module_id}/environment", "IMAGE_URL") or ""
    return image_url.rsplit("/", 1)[-1].split(":", 1)[0].split("@", 1)[0]


def mail_modules_on_node(rdb=None):
    """Other modules of this node that bind the public mail ports"""
    rdb = rdb or agent.redis_connect(use_replica=True)
    node_id = env("NODE_ID")
    found = []
    for module_id, mnode in (rdb.hgetall("cluster/module_node") or {}).items():
        if str(mnode) != str(node_id) or module_id == env("MODULE_ID"):
            continue
        if image_name_of(rdb, module_id) in MAIL_MODULE_IMAGES:
            found.append(module_id)
    return sorted(found)


def service_active():
    return subprocess.run(["systemctl", "--user", "-q", "is-active", SERVICE]).returncode == 0


def list_servers(rdb=None):
    """Service records of every Carbonio instance of the cluster"""
    rdb = rdb or agent.redis_connect(use_replica=True)
    servers = []
    for key in rdb.scan_iter("module/*/srv/tcp/carbonio"):
        module_id = key.split("/")[1]
        record = rdb.hgetall(key) or {}
        if record.get("fqdn"):
            record["module_id"] = module_id
            servers.append(record)
    for key in rdb.scan_iter("module/*/srv/tcp/carbonio-proxy"):
        module_id = key.split("/")[1]
        record = rdb.hgetall(key) or {}
        if record.get("fqdn"):
            record["module_id"] = module_id
            record["role"] = "proxy"
            servers.append(record)
    return sorted(servers, key=lambda r: r["module_id"])


def list_masters(rdb=None):
    """Masters that accept new servers: the choices of a joining server"""
    return [
        {
            "module_id": s["module_id"],
            "fqdn": s.get("fqdn", ""),
            "node": s.get("node", ""),
            "release": s.get("release", ""),
            "mail_domain": s.get("mail_domain", ""),
        }
        for s in list_servers(rdb)
        if s.get("role") == "master" and s.get("accept_join") == "1" and s["module_id"] != env("MODULE_ID")
    ]


def group_master():
    """Module id of the main server of this installation"""
    return env("CARBONIO_JOIN")


def hosts_entries(rdb=None):
    """'IP FQDN' lines of the other servers of the same installation"""
    master = group_master()
    lines = []
    for server in list_servers(rdb):
        if server["module_id"] == env("MODULE_ID"):
            continue
        same_group = server["module_id"] == master or server.get("master") == master
        if same_group and server.get("host") and server.get("fqdn"):
            lines.append(f"{server['host']} {server['fqdn']}")
    return sorted(set(lines))


def write_file_atomic(path, content, mode=0o644):
    tmp = f"{path}.{os.getpid()}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    with os.fdopen(fd, "w") as fout:
        fout.write(content)
    os.replace(tmp, path)


def write_hosts_file(rdb=None):
    os.makedirs("runtime", exist_ok=True)
    content = "".join(f"{line}\n" for line in hosts_entries(rdb))
    path = "runtime/hosts"
    try:
        with open(path) as fin:
            if fin.read() == content:
                return False
    except FileNotFoundError:
        pass
    write_file_atomic(path, content)
    return True


def publish_service():
    """Publish (or refresh) the service record of this instance"""
    rdb = agent.redis_connect(privileged=True)
    key = f"module/{env('MODULE_ID')}/srv/tcp/{SRV_NAME}"
    record = {
        "host": node_vpn_ip(rdb),
        "port": "443",
        "fqdn": env("CARBONIO_HOSTNAME"),
        "role": "proxy",
        "master": group_master(),
        "node": env("NODE_ID"),
        "release": env("CARBONIO_RELEASE"),
        "public_host": env("TRAEFIK_HOST"),
    }
    pipe = rdb.pipeline()
    pipe.delete(key)
    pipe.hset(key, mapping=record)
    pipe.publish(f"module/{env('MODULE_ID')}/event/carbonio-server-changed", json.dumps({
        "module_id": env("MODULE_ID"),
        "module_uuid": env("MODULE_UUID"),
        "master": record["master"],
    }))
    pipe.execute()


def podman_exec(args, stdin=None, check=True):
    """Run a command in the Carbonio container. Secrets go through stdin."""
    cmd = ["podman", "exec"] + (["-i"] if stdin is not None else []) + [CONTAINER] + args
    return subprocess.run(cmd, input=stdin, text=True, capture_output=True, check=check)


def carbonio_status():
    """Health of the services, from carbonio-status in the container"""
    try:
        proc = podman_exec(["/usr/local/sbin/carbonio-status"], check=False)
        return json.loads(proc.stdout or "{}")
    except (json.JSONDecodeError, OSError):
        return {}


#
# Sealed join bundle
#
# A joining server needs the passwords of the LDAP service accounts of the
# installation. Redis (where NS8 keeps task input and output for hours) is
# readable by every module, so they travel sealed: the joining server sends
# an ephemeral X25519 public key, the master encrypts the bundle for it
# (ECDH + HKDF-SHA256 + AES-256-GCM) and only the joining server, which
# never stores its private key, can open it.
#

def _derive_key(shared, salt):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt,
                info=b"ns8-carbonio join bundle v1").derive(shared)


def new_keypair():
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    private = X25519PrivateKey.generate()
    public = private.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return private, base64.b64encode(public).decode()


def seal_bundle(public_key_b64, payload):
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import serialization
    peer = X25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
    ephemeral = X25519PrivateKey.generate()
    epub = ephemeral.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    key = _derive_key(ephemeral.exchange(peer), epub)
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(key).encrypt(nonce, json.dumps(payload).encode(), epub)
    return {
        "ephemeral_public_key": base64.b64encode(epub).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }


def open_bundle(private_key, sealed):
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    epub = base64.b64decode(sealed["ephemeral_public_key"])
    key = _derive_key(private_key.exchange(X25519PublicKey.from_public_bytes(epub)), epub)
    plain = AESGCM(key).decrypt(base64.b64decode(sealed["nonce"]),
                                base64.b64decode(sealed["ciphertext"]), epub)
    return json.loads(plain)


def fetch_join_bundle(master_id):
    """Ask the master for the shared secrets. Returns (bundle, master_info)."""
    import agent.tasks
    private, public = new_keypair()
    response = agent.tasks.run(
        agent_id=f"module/{master_id}",
        action="seal-join-bundle",
        data={"public_key": public, "module_id": env("MODULE_ID"), "fqdn": env("CARBONIO_HOSTNAME")},
        extra={"isNotificationHidden": True},
    )
    if response["exit_code"] != 0:
        raise RuntimeError(f"seal-join-bundle on {master_id} failed with exit code {response['exit_code']}")
    output = response["output"]
    bundle = open_bundle(private, output["sealed"])
    return bundle, output.get("master", {})


#
# Debian version comparison (dpkg --compare-versions), for the release
# check of update-module: dpkg is not installed on every node
#

def _order(char):
    if char == "~":
        return -1
    if char.isdigit():
        return 0
    if not char:
        return 0
    if char.isalpha():
        return ord(char)
    return ord(char) + 256


def _compare_part(left, right):
    left, right = list(left), list(right)
    while left or right:
        first_diff = 0
        while (left and not left[0].isdigit()) or (right and not right[0].isdigit()):
            lc = _order(left[0]) if left and not left[0].isdigit() else 0
            rc = _order(right[0]) if right and not right[0].isdigit() else 0
            if lc != rc:
                return lc - rc
            if left and not left[0].isdigit():
                left.pop(0)
            if right and not right[0].isdigit():
                right.pop(0)
        lnum = ""
        while left and left[0].isdigit():
            lnum += left.pop(0)
        rnum = ""
        while right and right[0].isdigit():
            rnum += right.pop(0)
        first_diff = int(lnum or 0) - int(rnum or 0)
        if first_diff:
            return first_diff
    return 0


def _split_version(version):
    epoch, _, rest = version.rpartition(":") if ":" in version else ("0", "", version)
    upstream, _, revision = rest.rpartition("-") if "-" in rest else (rest, "", "0")
    return int(epoch or 0), upstream, revision


def compare_deb_versions(left, right):
    """Negative, zero or positive, like dpkg --compare-versions"""
    le, lu, lr = _split_version(left)
    re_, ru, rr = _split_version(right)
    if le != re_:
        return le - re_
    return _compare_part(lu, ru) or _compare_part(lr, rr)
