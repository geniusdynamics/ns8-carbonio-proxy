# Untitled string in Configure the Carbonio edge proxy Schema

```txt
http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/join
```

Module id of the ns8-carbonio main server to join. It cannot change after the first configuration.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module.json\*](carbonio-proxy/configure-module.json "open original schema") |

## join Type

`string`

## join Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^([a-z][a-z0-9-]*[0-9]+)?$
```

[try pattern](https://regexr.com/?expression=%5E\(%5Ba-z%5D%5Ba-z0-9-%5D*%5B0-9%5D%2B\)%3F%24 "try regular expression with regexr.com")
