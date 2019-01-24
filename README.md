# JWT Auth service + JWT Validation Service.


#### Auth Resource(login):

`POST /api/authorize`

```
{"email":"admin","password":"password"}
```

Returns a JWT token.

#### Private Resource:

`GET /api/private`

Returns the private resource if your `Authorization: Bearer <token>` is correct.
