# API Schema
```bash
Schema Version: v2 # Increase this number whenever the schema changes.
```

The interactions with the server and data storage in the database are all done using JSON objects. The file that contains code for these interactions should have the version number in a comment. This will make any API level incompability easily noticable.

## Connecting to the Server

Using zeroconf, look for this service: `assis10t._http._tcp.`

## Authentication

For requests that require authentication, include an http header called `"username"` with the username.

## Data Types:

```javascript
User {
    "_id": String,
    "username": String,
    "type": "merchant" or "customer" or "robot",
    "robotId": String // Only for type: robot
}

Item {
    "_id": String,
    "warehouseId": String,
    "name": String,
    "image": Base64 encoded String (or null for default image),
    "position": Position,
    "quantity": Double,
    "unit": String (or null if there is no unit),
    "price": Double // In GBP
}

Position {
    "x": Int, // Perpendicular to robot's initial position.
    "y": Int, // Parallel to robot's initial position.
    "z": Int // Vertical
}

Order {
    "_id": String,
    "userId": String,
    "warehouseId": String,
    "timestamp": String,
    "items": [Item],
    "status": "PENDING", "IN_TRANSIT", "COMPLETE", "CANCELED"
}

Warehouse {
    "_id": String,
    "merchantId": String, // The merchant that owns this warehouse.
    "name": String,
    "image": Base64 encoded String (or null for default image),
    "location": {
        "latitude": Double,
        "longitude": Double
    },
    "dimensions": {
        "x": Int, // Perpendicular to robot's initial position.
        "y": Int, // Parallel to robot's initial position.
        "z": [Double] // Vertical. Each element is height of a shelf, in ascending order, in meters. (Include bottom shelf as 0.0)
    },
    "items": [Item] // Only for GET /warehouse/:warehouseId
}

Robot {
    "_id": String,
    "warehouseId": String,
    "last_seen": ISO-8601 formatted date String,
    "status": "WAITING" or "ON_JOB" or "MIA" or "NOT_RESPONDING" or "MANUAL_CONTROL",
    "home_x": Int,
    "home_y": Int,
    "location": {
        "x": Int, // Perpendicular to robot's initial position.
        "y": Int, // Parallel to robot's initial position.
        "z": Int // Vertical
    }
}

Job {
    "_id": String,
    "start": Position,
    "finish": Position,
    "instruction_set": [Instruction]
}

// Instruction object can be one of the following:
Instruction {
    "command": "move",
    "parameters": {
        "blocks": Int, // Positive
        "direction": "forward" or "backward" or "left" or "right"
    }
}
// or
Instruction {
    "command": "lift",
    "parameters": {
        "height": Double // in meters
    }
}
// or
Instruction {
    "command": "grab",
    "parameters": {}
}
```


## API Endpoints

| Method | Path | Auth | Description |
|-|-|:-:|-
| `GET` | `/ping` | | Returns `Pong`. |
| `POST` | `/register` | | Registers a new `User`. |
| `POST` | `/login` | | Logs in existing `User`. |
| `GET` | `/order` | `Customer` | Gets all `Order`s of current `User`. |
| `GET` | `/order/:orderId` | `Customer` | Gets `Order` with given id. |
| `POST` | `/order` | `Customer` | Adds given `Order`. |
| `GET` | `/warehouse` | | Gets all `Warehouse`s. |
| `POST` | `/warehouse` | `Merchant` | Create/edit a warehouse. |
| `GET` | `/warehouse/:warehouseId` | | Gets given `Warehouse` with its items. |
| `POST` | `/warehouse/:warehouseId/items` | `Merchant` | Adds an `Item` to a `Warehouse`. |
| `GET` | `/warehouse/:warehouseId/orders` | `Merchant` | Gets all orders in the given `Warehouse`. |
| `GET` | `/warehouse/:warehouseId/robot` | `Merchant` | Gets the state of the robot(s). |
| `GET` | `/robot` | `Robot` | Get details of the current Robot. |
| `GET` | `/robot/:robotId` | `Merchant` | Get details about the robot with given `robotId` |
| `POST` | `/robot/:robotId/sethome` | `Merchant` | Set the home location of the robot. |
| `GET` | `/robotjob` | `Robot` | Gets the next job the robot needs to do. |
| `PUT` | `/turnon/:n` | | Starts moving the robot. Robot stops after seeing `n` markers. |
| `PUT` | `/turnoff` | | Stops the robot. |
#### Error Handling
All requests that complete successfully respond with a JSON object with `"success": true`. Any failure to fulfill the request results in the following response with an appropriate status code >= 400:
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
pong
```

#### `POST /register`
```javascript
===== Input =====
{
    "username": String,
    "type": "merchant" or "customer" or "robot"
}
===== Output =====
{
    "success": Boolean,
    "user": User
}
```

#### `POST /login`
```javascript
===== Input =====
{
    "username": String
}
===== Output =====
{
    "success": true,
    "user": User
}
```

#### `GET /order`
```javascript
===== Output =====
{
    "success": true,
    "orders": [Order]
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
    "success": true
}
```

#### `GET /warehouse`
```javascript
===== Output =====
{
    "success": true,
    "warehouses": [Warehouse]
}
```

#### `POST /warehouse`
```javascript
===== Input =====
Warehouse //With _id if updating an existing warehouse, or without _id if creating a new one.
===== Output =====
{
    "success": true,
    "warehouse": Warehouse
}
```

#### `GET /warehouse/:warehouseId`
```javascript
===== Output =====
{
    "success": true,
    "warehouse": Warehouse // Including list of items in the warehouse.
}
```

#### `POST /warehouse/:warehouseId/items`
```javascript
===== Input =====
Item //With _id if updating an existing item, or without _id if creating a new one.
===== Output =====
{
    "success": true,
    "item": Item
}
```

#### `GET /warehouse/:warehouseId/orders`
```javascript
===== Output =====
{
    "success": true,
    "orders": [Order]
}
```

#### `GET /warehouse/:warehouseId/robot`
```javascript
===== Output =====
{
    "success": true,
    "robots": [Robot]
}
```

#### `GET /robot`
```javascript
===== Output =====
{
    "success": true,
    "robot": Robot
}
```

#### `GET /robot/:robotId`
```javascript
===== Output =====
{
    "success": true,
    "robot": Robot
}
```

#### `POST /robot/:robotId/sethome`
```javascript
===== Input =====
Position
===== Output =====
{
    "success": true
}
```

#### `GET /robotjob`
```javascript
===== Output =====
{
    "success": true,
    "job": Job
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
