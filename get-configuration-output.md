# Get the Carbonio edge proxy configuration Schema

```txt
http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json](carbonio-proxy/get-configuration-output.json "open original schema") |

## Get the Carbonio edge proxy configuration Type

`object` ([Get the Carbonio edge proxy configuration](get-configuration-output.md))

# Get the Carbonio edge proxy configuration Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                      |
| :-------------------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [host](#host)                           | `string`  | Required | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-host.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/host")                           |
| [http2https](#http2https)               | `boolean` | Optional | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-http2https.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/http2https")               |
| [lets_encrypt](#lets_encrypt)           | `boolean` | Optional | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-lets_encrypt.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/lets_encrypt")           |
| [join](#join)                           | `string`  | Required | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-join.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/join")                           |
| [admin_host](#admin_host)               | `string`  | Optional | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-admin_host.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/admin_host")               |
| [initialized](#initialized)             | `boolean` | Required | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-initialized.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/initialized")             |
| [release](#release)                     | `string`  | Optional | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-release.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/release")                     |
| [ldap_secrets_set](#ldap_secrets_set)   | `boolean` | Optional | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-ldap_secrets_set.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/ldap_secrets_set")   |
| [available_masters](#available_masters) | `array`   | Required | cannot be null | [Get the Carbonio edge proxy configuration](get-configuration-output-properties-available_masters.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/available_masters") |

## host



`host`

* is required

* Type: `string`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-host.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/host")

### host Type

`string`

## http2https



`http2https`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-http2https.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/http2https")

### http2https Type

`boolean`

## lets_encrypt



`lets_encrypt`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-lets_encrypt.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/lets_encrypt")

### lets_encrypt Type

`boolean`

## join



`join`

* is required

* Type: `string`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-join.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/join")

### join Type

`string`

## admin_host



`admin_host`

* is optional

* Type: `string`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-admin_host.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/admin_host")

### admin_host Type

`string`

## initialized



`initialized`

* is required

* Type: `boolean`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-initialized.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/initialized")

### initialized Type

`boolean`

## release



`release`

* is optional

* Type: `string`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-release.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/release")

### release Type

`string`

## ldap_secrets_set



`ldap_secrets_set`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-ldap_secrets_set.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/ldap_secrets_set")

### ldap_secrets_set Type

`boolean`

## available_masters



`available_masters`

* is required

* Type: `object[]` ([Details](get-configuration-output-properties-available_masters-items.md))

* cannot be null

* defined in: [Get the Carbonio edge proxy configuration](get-configuration-output-properties-available_masters.md "http://schema.nethserver.org/carbonio-proxy/get-configuration-output.json#/properties/available_masters")

### available_masters Type

`object[]` ([Details](get-configuration-output-properties-available_masters-items.md))
