# Configure the Carbonio edge proxy Schema

```txt
http://schema.nethserver.org/carbonio-proxy/configure-module.json
```

Configure a Carbonio CE edge proxy joined to a ns8-carbonio main server

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [configure-module.json](carbonio-proxy/configure-module.json "open original schema") |

## Configure the Carbonio edge proxy Type

`object` ([Configure the Carbonio edge proxy](configure-module.md))

## Configure the Carbonio edge proxy Examples

```json
{
  "host": "webmail.example.org",
  "lets_encrypt": true,
  "http2https": true,
  "join": "carbonio1"
}
```

# Configure the Carbonio edge proxy Properties

| Property                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                    |
| :---------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [host](#host)                 | `string`  | Required | cannot be null | [Configure the Carbonio edge proxy](configure-module-properties-host.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/host")                 |
| [lets_encrypt](#lets_encrypt) | `boolean` | Optional | cannot be null | [Configure the Carbonio edge proxy](configure-module-properties-lets_encrypt.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/lets_encrypt") |
| [http2https](#http2https)     | `boolean` | Optional | cannot be null | [Configure the Carbonio edge proxy](configure-module-properties-http2https.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/http2https")     |
| [join](#join)                 | `string`  | Optional | cannot be null | [Configure the Carbonio edge proxy](configure-module-properties-join.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/join")                 |
| [admin_host](#admin_host)     | `string`  | Optional | cannot be null | [Configure the Carbonio edge proxy](configure-module-properties-admin_host.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/admin_host")     |

## host

Host name (FQDN) of the proxy: web client and IMAP/POP3 server name. It cannot change after the first configuration.

`host`

* is required

* Type: `string`

* cannot be null

* defined in: [Configure the Carbonio edge proxy](configure-module-properties-host.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/host")

### host Type

`string`

### host Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
\.
```

[try pattern](https://regexr.com/?expression=%5C. "try regular expression with regexr.com")

**hostname**: the string must be a hostname, according to [RFC 1123, section 2.1](https://tools.ietf.org/html/rfc1123 "check the specification")

## lets_encrypt

Request a Let's Encrypt certificate for the host name, also used by IMAP and POP3

`lets_encrypt`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [Configure the Carbonio edge proxy](configure-module-properties-lets_encrypt.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/lets_encrypt")

### lets_encrypt Type

`boolean`

## http2https

Redirect HTTP to HTTPS

`http2https`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [Configure the Carbonio edge proxy](configure-module-properties-http2https.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/http2https")

### http2https Type

`boolean`

## join

Module id of the ns8-carbonio main server to join. It cannot change after the first configuration.

`join`

* is optional

* Type: `string`

* cannot be null

* defined in: [Configure the Carbonio edge proxy](configure-module-properties-join.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/join")

### join Type

`string`

### join Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^([a-z][a-z0-9-]*[0-9]+)?$
```

[try pattern](https://regexr.com/?expression=%5E\(%5Ba-z%5D%5Ba-z0-9-%5D*%5B0-9%5D%2B\)%3F%24 "try regular expression with regexr.com")

## admin_host

Optional host name (FQDN) that Traefik routes to the Carbonio Admin Panel through this proxy; empty: no route

`admin_host`

* is optional

* Type: `string`

* cannot be null

* defined in: [Configure the Carbonio edge proxy](configure-module-properties-admin_host.md "http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/admin_host")

### admin_host Type

`string`

### admin_host Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$|^$
```

[try pattern](https://regexr.com/?expression=%5E\(%5Ba-zA-Z0-9%5D\(%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D\)%3F%5C.\)%2B%5Ba-zA-Z%5D%7B2%2C%7D%24%7C%5E%24 "try regular expression with regexr.com")
