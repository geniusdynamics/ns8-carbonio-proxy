# Carbonio health Schema

```txt
http://schema.nethserver.org/carbonio/get-health-output.json
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-health-output.json](carbonio/get-health-output.json "open original schema") |

## Carbonio health Type

`object` ([Carbonio health](get-health-output.md))

# Carbonio health Properties

| Property                          | Type      | Required | Nullable       | Defined by                                                                                                                                                  |
| :-------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [healthy](#healthy)               | `boolean` | Required | cannot be null | [Carbonio health](get-health-output-properties-healthy.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/healthy")               |
| [service_active](#service_active) | `boolean` | Required | cannot be null | [Carbonio health](get-health-output-properties-service_active.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/service_active") |
| [phase](#phase)                   | `string`  | Required | cannot be null | [Carbonio health](get-health-output-properties-phase.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/phase")                   |
| [release](#release)               | `string`  | Optional | cannot be null | [Carbonio health](get-health-output-properties-release.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/release")               |
| [services](#services)             | `object`  | Required | cannot be null | [Carbonio health](get-health-output-properties-services.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/services")             |
| [error](#error)                   | `string`  | Optional | cannot be null | [Carbonio health](get-health-output-properties-error.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/error")                   |
| [cluster_role](#cluster_role)     | `string`  | Optional | cannot be null | [Carbonio health](get-health-output-properties-cluster_role.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/cluster_role")     |
| [servers](#servers)               | `array`   | Optional | cannot be null | [Carbonio health](get-health-output-properties-servers.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/servers")               |
| [store_disk](#store_disk)         | `object`  | Optional | cannot be null | [Carbonio health](get-health-output-properties-store_disk.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/store_disk")         |

## healthy



`healthy`

* is required

* Type: `boolean`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-healthy.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/healthy")

### healthy Type

`boolean`

## service_active



`service_active`

* is required

* Type: `boolean`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-service_active.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/service_active")

### service_active Type

`boolean`

## phase



`phase`

* is required

* Type: `string`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-phase.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/phase")

### phase Type

`string`

## release



`release`

* is optional

* Type: `string`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-release.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/release")

### release Type

`string`

## services



`services`

* is required

* Type: `object` ([Details](get-health-output-properties-services.md))

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-services.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/services")

### services Type

`object` ([Details](get-health-output-properties-services.md))

## error



`error`

* is optional

* Type: `string`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-error.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/error")

### error Type

`string`

## cluster_role



`cluster_role`

* is optional

* Type: `string`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-cluster_role.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/cluster_role")

### cluster_role Type

`string`

## servers



`servers`

* is optional

* Type: `array`

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-servers.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/servers")

### servers Type

`array`

## store_disk



`store_disk`

* is optional

* Type: `object` ([Details](get-health-output-properties-store_disk.md))

* cannot be null

* defined in: [Carbonio health](get-health-output-properties-store_disk.md "http://schema.nethserver.org/carbonio/get-health-output.json#/properties/store_disk")

### store_disk Type

`object` ([Details](get-health-output-properties-store_disk.md))
