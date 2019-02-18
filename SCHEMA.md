# API Schema
```bash
Schema Version: v1 # Increase this number whenever the schema changes.
```

The interactions with the server and data storage in the database are all done using JSON objects. The file that contains code for these interactions should have the version number in a comment. This will make any API level incompability easily noticable.

## Connecting to the Server

Using zeroconf, look for this service: `assis10t._http._tcp.`

## Data Types:

```javascript
User {
    "_id": String,
    "username": String
}

Item {
    "_id": String,
    "warehouseId": String,
    "name": String,
    "quantity": Double,
    "unit": String (or null if there is no unit)
}

Order {
    "_id": String,
    "userId": String,
    "warehouseId": String,
    "items": [Item]
}

Warehouse {
    "_id": String,
    "location": String // String to be used for the Google Maps API query
}
```


## API Endpoints

| Method | Path | Description |
|-|-|-|
| `GET` | `/ping` | Returns `Pong`. |
| `GET` | `/order` | Gets all `Order`s. |
| `GET` | `/order/:orderId` | Gets `Order` with given id. |
| `POST` | `/order` | Adds given `Order`. Starts moving robot. |
| `GET` | `/jobs` | Gets all `Job`s. |
| `POST` | `/jobs` | Adds given `Job`. |
| `GET` | `/items` | Gets all `Item`s. |
| `POST` | `/items` | Adds `Item`. |
| `PUT` | `/turnon/:n` | Starts moving the robot. Robot stops after seeing `n` markers. |
| `PUT` | `/turnoff` | Stops the robot. |
| `GET` | `/getmovement` | Gets the current task for the robot. |
| `POST` | `/register` | Registers a new user. |
| `POST` | `/login` | Logs in existing user. |

#### Any Server Error (Status 500)
```javascript
===== Output =====
{
    "success": false,
    "error": String
}
```

#### `GET /ping`
```javascript
===== Output =====
"pong"
```

#### `GET /order`
```javascript
===== Output =====
{
    "success": true,
    "orders": [Order] (or null if no orders found)
}
```

#### `GET /order/:orderId`
```javascript
===== Output =====
{
    "success": true,
    "orders": Order (or null if order isnt found)
}
```

#### `POST /order`
```javascript
===== Input =====
Order // without _id field

===== Output =====
{
    "success": Boolean
}
```

#### `GET /jobs`
```javascript
===== Output =====
{
    "success": Boolean,
    "jobs": [Job] (or null if no jobs found)
}
```

#### `POST /jobs`
```javascript
===== Input =====
Job // without _id field

===== Output =====
{
    "success": Boolean
}
```

#### `GET /items`
```javascript
===== Output =====
{
    "success": Boolean,
    "items": [Item] (or null if no items found)
}
```

#### `POST /items`
```javascript
===== Input =====
Item // without _id field

===== Output =====
{
    "success": Boolean
}
```

#### `PUT /turnon/:n`
```javascript
===== Output =====
{
    "success": true
}
```

#### `PUT /turnoff`
```javascript
===== Output =====
{
    "success": true
}
```

#### `GET /getmovement`
```javascript
===== Output =====
{
    "success": true,
    "status": {
        "moving": Boolean,
        "markers": Int (or null if not moving)
    }
}
```

#### `POST /register`
```javascript
===== Output =====
{
    "success": Boolean
}
```

#### `POST /login`
```javascript
===== Output =====
{
    "success": true,
    "loggedIn": Boolean
}
```