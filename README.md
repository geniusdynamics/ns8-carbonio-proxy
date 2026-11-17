# ns8-carbonio-proxy

An edge proxy for a multi-server [Carbonio CE](https://www.zextras.com/carbonio-community-edition/)
installation built with [ns8-carbonio](https://github.com/geniusdynamics/ns8-carbonio)
on [NethServer 8](https://github.com/NethServer/ns8-core).

The proxy is an extra entry point to the installation, on a node of its own. It
serves webmail, the Admin Panel, IMAP and POP3, and sends every user to the
mailbox server that holds their mailbox.

> **Unofficial.** Genius Dynamics builds this module from the public Carbonio CE
> packages. Zextras does not endorse it. "Carbonio" and "Zextras" are trademarks
> of Zextras.

**A single business does not need this module.** A single ns8-carbonio server
already includes the Carbonio proxy, and owns the mail ports of its node.

**Experimental.** Multi-server behaviour was tested with containers on one host.
The CI checks only installation, validation and removal, because one test node
cannot run both a main server and a proxy.

## Contents

- [How it works](#how-it-works)
- [Setup](#setup)
- [Ports](#ports)
- [Redis key contract](#redis-key-contract)
- [Secrets](#secrets)
- [Backup](#backup)
- [Updates](#updates)
- [Known limits](#known-limits)
- [Licences](#licences)
- [Debug](#debug)

## How it works

This module runs the Carbonio **proxy role** (nginx and memcached), in the same
container image as ns8-carbonio, built from the public Carbonio CE packages.
See [server/](server). That directory is kept identical to the one in
ns8-carbonio.

At its first start the proxy joins the directory (LDAP) of an ns8-carbonio
**main server**. From then on, Carbonio's own route lookup finds the right
mailbox server for each login, so the module writes no upstream list. A mailbox
server added later is routed as soon as it exists in the directory.

The proxy also needs to resolve the host names of the main server and of every
additional mailbox server to their WireGuard addresses. It reads them from the
Redis service records and refreshes them live:

- on the `carbonio-server-changed` event,
- on the `module-removed` event.

The container is not restarted for this.

What stays elsewhere:

- **Traefik** keeps ports 80 and 443 of the node, and forwards the web client
  to the proxy.
- **SMTP** (inbound mail, submission on 587 and 465) stays on the main server.
  The Carbonio proxy does not proxy SMTP.

## Setup

1. Set up the main server. On one node, configure ns8-carbonio as *Main server
   of a multi-server installation*, with *Accept new servers* on. Optionally,
   add mailbox servers on other nodes.
2. Install the proxy on another node. That node must not run another mail
   application:

       add-module ghcr.io/geniusdynamics/carbonio-proxy:latest 1

3. Configure the proxy in *Settings*. Choose the main server from the list (it
   shows the main servers of the same Carbonio release), then set the host name
   of the proxy. Or from the command line:

   ```bash
   api-cli run module/carbonio-proxy1/configure-module --data '{"host":"webmail.example.org","join":"carbonio1","lets_encrypt":true}'
   ```

4. Point users at the proxy. In DNS, point the webmail and IMAP/POP3 names at
   the proxy node. MX records keep pointing at the main server.

The *Status* page, and the `get-health` action, show the state of the proxy
services and the servers of the installation.

## Ports

| Port | Bound on |
|---|---|
| 110, 143, 993, 995 | every node address, opened in the firewall |
| web client (443 in the container) | 127.0.0.1, `TCP_PORTS[0]`, behind Traefik |
| Admin Panel (6071 in the container) | 127.0.0.1, `TCP_PORTS[1]`, behind Traefik when an Admin Panel host name is set |

Configuration is refused when another mail module (ns8-carbonio, ns8-mail,
mailcow and others) is on the node, or when one of these ports is in use.
Connections in TIME_WAIT do not count as in use.

## Redis key contract

Each proxy publishes a non-secret record:

```
module/<module_id>/srv/tcp/carbonio-proxy   (hash)
  host         WireGuard address of the node
  fqdn         Carbonio server name of the proxy
  role         proxy
  master       module id of the main server
  node         node id
  release      Carbonio release
  public_host  web host name
```

It reads the `module/*/srv/tcp/carbonio` records of the ns8-carbonio servers.
That contract is documented in the ns8-carbonio README.

## Secrets

The proxy receives the passwords of the directory service accounts from the
main server as a sealed bundle:

1. The proxy creates an ephemeral X25519 key pair and sends the public key with
   its `seal-join-bundle` request.
2. The main server encrypts the bundle for that key, with ECDH, then
   HKDF-SHA256, then AES-256-GCM.
3. The proxy decrypts it and writes the passwords to `state/secrets.env`, with
   mode 0600.

The passwords never reach Redis in clear. Only modules holding the
`carbonio-peer` role on the main server can call that action. The proxy has
that role through its image label `carbonio@any:carbonio-peer`.

`get-configuration` returns only a `ldap_secrets_set` boolean.

## Backup

The backup includes:

- `state/secrets.env`,
- the configuration, data and certificate volumes.

The proxy holds no mail. On restore, the proxy joins the same main server again.

## Updates

- The same release check as ns8-carbonio runs: a downgrade of the Carbonio
  packages is refused, and the running release is kept.
- Update the main server first, then the mailbox servers, then the proxies.
- A proxy joins only a main server of the same release.

## Known limits

- **Stale routes after a mailbox move.** From Carbonio 26.3, memcached listens
  only on the loopback, and the purge of the route cache by the mailbox servers
  moved to the Carbonio Mesh, which this release does not run. After a mailbox
  moves to another server, a cached route can last until it expires
  (`zimbraReverseProxyCacheEntryTTL`). To clear the cache earlier, restart the
  proxy.
- **No SMTP.** Only webmail, Admin Panel, IMAP and POP3 go through the proxy.

## Licences

- **The module** is under GPL-3.0-or-later.
- **The runtime image** contains the unmodified Carbonio CE packages, under
  GPL-2.0-only and AGPL-3.0-only, with their licence texts in `/usr/share/doc`.
  Their source code is at https://github.com/zextras.
- **No proprietary package is included.** The proprietary `pending-setups` is
  replaced by a no-op stand-in.

## Debug

```bash
runagent -m carbonio-proxy1 systemctl --user status carbonio
runagent -m carbonio-proxy1 podman exec carbonio carbonio-status
journalctl _UID=$(id -u carbonio-proxy1) -t carbonio -f
```
