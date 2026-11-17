# Untitled string in Configure the Carbonio edge proxy Schema

```txt
http://schema.nethserver.org/carbonio-proxy/configure-module.json#/properties/admin_host
```

Optional host name (FQDN) that Traefik routes to the Carbonio Admin Panel through this proxy; empty: no route

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module.json\*](carbonio-proxy/configure-module.json "open original schema") |

## admin_host Type

`string`

## admin_host Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$|^$
```

[try pattern](https://regexr.com/?expression=%5E\(%5Ba-zA-Z0-9%5D\(%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D\)%3F%5C.\)%2B%5Ba-zA-Z%5D%7B2%2C%7D%24%7C%5E%24 "try regular expression with regexr.com")
