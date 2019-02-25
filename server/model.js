const db = require('./db')
const assert = require('assert')
const ObjectID = require('mongodb').ObjectID
const factory = db => ({
    getOrders: userId =>
        db()
            .collection('orders')
            .find({ userId })
            .toArray(),
    getOrderById: orderId =>
        db()
            .collection('orders')
            .findOne({ _id: ObjectID(orderId) }),
    addOrder: orderData =>
        // TODO: Check stock before finishing the order.
        db()
            .collection('orders')
            .insertOne(orderData)
            .then(() => Promise.all(orderData.items.map(i => factory(db).removeItem(i))))
            .then(() => factory(db).turnOn(1))
            .then(() => orderData),
    turnOn: markers =>
        db()
            .collection('bob_movement')
            .updateOne({}, { $set: { moving: true, markers: parseInt(markers) } })
            .then(() => 'on'),
    turnOff: () =>
        db()
            .collection('bob_movement')
            .updateOne({}, { $set: { moving: false } })
            .then(() => 'off'),
    getMovement: () =>
        db()
            .collection('bob_movement')
            .findOne(),
    getWarehouses: () =>
        db()
            .collection('warehouses')
            .find()
            .toArray(),
    addWarehouse: warehouse => {
        if (!warehouse._id) {
            warehouse = { _id: new ObjectID(), ...warehouse }
            return db()
                .collection('warehouses')
                .insertOne(warehouse)
                .then(() => warehouse)
        } else {
            return db()
                .collection('warehouses')
                .updateOne({ _id: warehouse._id }, { $set: warehouse })
                .then(modifiedCount => (modifiedCount ? warehouse : null))
        }
    },
    getWarehouseById: async warehouseId => {
        const warehouse = await db()
            .collection('warehouses')
            .findOne({ _id: ObjectID(warehouseId) })
        if (!warehouse) return null

        const items = await factory(db).getItemsByWarehouseId(warehouseId)
        return {
            ...warehouse,
            items
        }
    },
    getItemsByWarehouseId: warehouseId =>
        db()
            .collection('inventory')
            .find({ warehouseId })
            .toArray(),
    getOrdersByWarehouseId: warehouseId =>
        db()
            .collection('orders')
            .find({ warehouseId })
            .toArray(),
    addItem: item => {
        if (!item._id) {
            item = { _id: new ObjectID(), ...item }
            return db()
                .collection('inventory')
                .insertOne(item)
                .then(() => item)
        } else {
            return db()
                .collection('inventory')
                .updateOne({ _id: ObjectID(item._id) }, { $set: item })
                .then(modifiedCount => (modifiedCount ? item : null))
        }
    },
    removeItem: item =>
        db()
            .collection('inventory')
            .deleteOne({ _id: ObjectID(item._id) }),
    createUser: (username, type) => {
        const user = { _id: new ObjectID(), username, type }
        return db()
            .collection('users')
            .insertOne(user)
            .then(() => user)
    },
    authUser: username =>
        db()
            .collection('users')
            .findOne({ username })
})

module.exports = factory(db)

module.exports.factory = factory
