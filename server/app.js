const bodyParser = require('body-parser')
const express = require('express')
const model = require('./model')
const cors = require('cors')

const auth = require('./auth')

const API_LEVEL = 'v3'

const app = express()

app.use(bodyParser.json({ limit: '50mb' }))

app.use(express.static('./public'))

const whitelist = ['http://localhost:3000', 'http://sdp-10-beta.herokuapp.com', 'https://sdp-10-beta.herokuapp.com']
app.use(
    cors({
        origin: (origin, callback) => {
            if (whitelist.indexOf(origin) > -1) {
                callback(null, true)
            } else {
                console.log(origin, 'is not allowed by CORS. Bypassing anyway.')
                callback(null, true)
            }
        },
        credentials: true
    })
)

//Logs all requests.
app.use((req, res, next) => {
    console.log(`${req.ip}: ${req.method} ${req.originalUrl}`)
    next()
})

app.get('/api/ping', (req, res) => {
    res.send('pong')
})
app.get(
    '/api/order',
    auth.customer((req, res, next) =>
        model
            .getOrders(req.user._id)
            .then(async orders => {
                const warehouses = await Promise.all(orders.map(order => model.getWarehouseById(order.warehouseId)))
                const newOrders = orders.map((order, i) => ({
                    ...order,
                    warehouse: warehouses[i]
                }))
                return newOrders
            })
            .then(orders => res.json({ success: true, orders }))
            .catch(next)
    )
)

app.get(
    '/api/order/:orderId',
    auth.customer((req, res, next) =>
        model
            .getOrderById(req.params.orderId)
            .then(order => {
                if (order && req.user._id.equals(order.userId)) {
                    model.getWarehouseById(order.warehouseId).then(warehouse => {
                        res.json({ success: true, order: { ...order, warehouse } })
                    })
                } else if (order)
                    res.status(403).json({ success: false, error: 'You cannot view details on this order.' })
                else res.status(404).json({ success: true, order: null })
            })
            .catch(next)
    )
)
// TODO: Check if ordered items exist.
app.post(
    '/api/order',
    auth.customer((req, res, next) => {
        const order = {
            ...req.body,
            userId: req.user._id,
            timestamp: new Date().toISOString()
        }
        model
            .addOrder(order)
            .then(order => res.json({ success: true, order }))
            .catch(next)
    })
)
app.get('/api/warehouse', (req, res, next) => {
    model
        .getWarehouses()
        .then(warehouses => res.json({ success: true, warehouses }))
        .catch(next)
})
app.post(
    '/api/warehouse',
    auth.merchant((req, res, next) => {
        model
            .addWarehouse({ ...req.body, merchantId: req.user._id })
            .then(warehouse => res.json({ success: true, warehouse }))
            .catch(next)
    })
)
app.get('/api/warehouse/:warehouseId', (req, res, next) => {
    model
        .getWarehouseWithItemsById(req.params.warehouseId)
        .then(warehouse => res.status(warehouse ? 200 : 404).json({ success: true, warehouse }))
        .catch(next)
})

app.post(
    '/api/warehouse/:warehouseId/items',
    auth.merchant((req, res, next) => {
        model
            .getWarehouseById(req.params.warehouseId)
            .then(warehouse => {
                if (!warehouse) {
                    res.status(404).json({
                        success: false,
                        error: 'Warehouse not found.'
                    })
                    throw null
                }
                if (!req.user._id.equals(warehouse.merchantId)) {
                    res.status(403).json({
                        success: false,
                        error: 'You cannot modify items in a warehouse you dont own.'
                    })
                    throw null
                }
                return model.addItem({ ...req.body, warehouseId: req.params.warehouseId })
            })
            .then(item => res.json({ success: true, item }))
            .catch(err => err && next(err))
    })
)
app.get(
    '/api/warehouse/:warehouseId/items/:itemId',
    auth.merchant((req, res, next) => {
        model
            .getItemById(req.params.itemId)
            .then(item => {
                if (!item) {
                    res.status(404).json({ success: false, error: 'Item not found.' })
                    throw null
                }
                return model.getWarehouseById(item.warehouseId).then(warehouse => {
                    if (!req.user._id.equals(warehouse.merchantId)) {
                        res.status(403).json({ success: false, error: 'You are not allowed to access this resource.' })
                        throw null
                    }
                    return item
                })
            })
            .then(item => res.json({ success: true, item }))
            .catch(err => err && next(err))
    })
)
app.delete(
    '/api/warehouse/:warehouseId/items/:itemId',
    auth.merchant((req, res, next) => {
        model
            .getItemById(req.params.itemId)
            .then(item => {
                if (!item) {
                    res.status(404).json({ success: false, error: 'Item not found.' })
                    throw null
                }
                return model.getWarehouseById(item.warehouseId)
            })
            .then(warehouse => {
                if (!req.user._id.equals(warehouse.merchantId)) {
                    res.status(403).json({ success: false, error: 'You are not allowed to access this resource.' })
                    throw null
                }
                return req.params.itemId
            })
            .then(itemId => model.deleteItemById(itemId))
            .then(() => res.json({ success: true }))
            .catch(err => err && next(err))
    })
)
app.get(
    '/api/warehouse/:warehouseId/orders',
    auth.merchant((req, res, next) => {
        model
            .getOrdersByWarehouseId(req.params.warehouseId)
            .then(orders => res.json({ success: true, orders }))
            .catch(next)
    })
)

app.get(
    '/api/warehouse/:warehouseId/orders/:orderId',
    auth.merchant((req, res, next) => {
        model
            .getOrderById(req.params.orderId)
            .then(order => {
                if (order && req.params.warehouseId === order.warehouseId) {
                    model.getWarehouseById(order.warehouseId).then(warehouse => {
                        if (req.user._id.equals(warehouse.merchantId)) {
                            res.json({ success: true, order: { ...order, warehouse } })
                        } else {
                            res.status(403).json({ success: false, error: 'You cannot view details on this order.' })
                        }
                    })
                } else if (order)
                    res.status(403).json({ success: false, error: 'You cannot view details on this order.' })
                else res.status(404).json({ success: true, order: null })
            })
            .catch(next)
    })
)

app.post(
    '/api/warehouse/:warehouseId/orders/:orderId',
    auth.merchant((req, res, next) =>
        model
            .getOrderById(req.params.orderId)
            .then(order => {
                if (order && req.params.warehouseId === order.warehouseId) {
                    model.getWarehouseById(order.warehouseId).then(warehouse => {
                        if (req.user._id.equals(warehouse.merchantId)) {
                            model
                                .setOrderStatus(req.params.orderId, req.body.status)
                                .then(res.json({ success: true, order: { ...order, warehouse } }))
                        } else {
                            res.status(403).json({ success: false, error: 'You cannot view details on this order.' })
                        }
                    })
                } else if (order)
                    res.status(403).json({ success: false, error: 'You cannot view details on this order.' })
                else res.status(404).json({ success: false, error: 'Order not found.' })
            })
            .catch(next)
    )
)

app.put('/api/turnon/:nOfMarkers', (req, res, next) => {
    const markers = req.params.nOfMarkers
    model
        .turnOn(markers)
        .then(on => res.json({ success: true, on }))
        .catch(next)
})
app.put('/api/turnoff', (req, res, next) => {
    model
        .turnOff()
        .then(off => res.json({ success: true, off }))
        .catch(next)
})
app.get('/api/getmovement', (req, res, next) => {
    model
        .getMovement()
        .then(status => res.json({ success: true, status }))
        .catch(next)
})
app.post('/api/register', (req, res, next) => {
    model
        .createUser(req.body.username, req.body.type)
        .then(user => {
            if (req.body.type == 'robot') {
                model
                    .addRobot(user.username, 0, 0)
                    .then(res.json({ success: true, user }))
                    .catch(next)
            } else {
                res.json({ success: true, user })
            }
        })
        .catch(next)
})
app.post('/api/login', (req, res, next) => {
    model.authUser(req.body.username).then(user => {
        if (user) res.json({ success: true, user })
        else res.status(401).json({ success: false, error: 'Username or password is incorrect.' })
    })
})
app.get(
    '/api/robot',
    auth.robot((req, res, next) => {
        var currentUser = req.user
        model
            .getRobot(currentUser.username)
            .then(robot => res.json({ success: true, robot }))
            .catch(next)
    })
)

app.get(
    '/api/robot/:robotId',
    auth.merchant((req, res, next) => {
        model
            .getRobot(req.params.robotId)
            .then(robot => res.json({ success: true, robot }))
            .catch(next)
    })
)
app.post(
    '/api/robot/:robotid/sethome',
    auth.merchant((req, res, next) => {
        model
            .setHome(req.params.robotid, req.body.home_x, req.body.home_y)
            .then(robot => res.json({ success: true, robot }))
            .catch(next)
    })
)

app.get(
    '/api/robotjob',
    auth.robot((req, res, next) => {
        model
            .getNextJob(req.user.username)
            .then(job => res.json({ success: true, job }))
            .catch(next)
    })
)

// For imaging the database and updating fake_db.json
app.get('/api/db', (req, res, next) => {
    model
        .getWholeDB()
        .then(data => res.json(data))
        .catch(next)
})

//Logs all responses.
app.use((req, res, next) => {
    console.log(`${req.ip}: ${req.method} ${req.originalUrl} response: ${res.body || ''}`)
    next()
})

//Logs errors and responds properly.
app.use((err, req, res, next) => {
    console.error(err.stack)
    res.status(500).json({ success: false, error: err.stack })
    next()
})

module.exports = app
module.exports.API_LEVEL = API_LEVEL
