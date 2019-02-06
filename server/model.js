const db = require('./db')
const assert = require('assert')
const ObjectID = require('mongodb').ObjectID
const factory = db => ({
    getAllOrders: () =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs)
                })
        }),
    getOrderById: orderId =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .find({ _id: new ObjectID(orderId) })
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs[0])
                })
        }),
    addOrder: orderData =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .insertOne(orderData, (err, order) => {
                    if (err) {
                        rej(err)
                        return
                    }
                    Promise.all(orderData.items.map(i => factory(db).removeItem(i)))
                        .then(() => factory(db).turnOn(1))
                        .then(() => res(orderData))
                        .catch(err => rej(err))
                })
        }),
    addJob: jobData =>
        new Promise((res, rej) => {
            db()
                .collection('jobs')
                .insertOne(jobData, (err, job) => {
                    err ? rej(err) : res(jobData)
                })
        }),
    getAllJobs: () =>
        new Promise((res, rej) => {
            db()
                .collection('jobs')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs)
                })
        }),
    turnOn: markers =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .updateOne(
                    { _id: 'movement' },
                    { $set: { moving: true, markers: parseInt(markers) } },
                    (err, count_modified) => {
                        err ? rej(err) : res('on')
                    }
                )
        }),
    turnOff: () =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .updateOne({ _id: 'movement' }, { $set: { moving: false } }, (err, count_modified) => {
                    err ? rej(err) : res('off')
                })
        }),
    getMovement: () =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs[0])
                })
        }),

    addItem: item =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .insertOne({ _id: new ObjectID(), ...item }, (err, item) => {
                    err ? rej(err) : res(item)
                })
        }),
    removeItem: item =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .deleteOne({ _id: new ObjectID(item._id) }, (err, item) => {
                    err ? rej(err) : res(item)
                })
        }),
    getItems: () =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .find({})
                .toArray((err, items) => {
                    err ? rej(err) : res(items)
                })
        }),
    createUser: (uname, pass) =>
        new Promise((res, rej) => {
            db()
                .collection('users')
                .insertOne({ _id: new ObjectID(), username: uname, password: pass }, (err, user) => {
                    err ? rej(err) : res(user)
                })
        }),
    authUser: (uname, pass) =>
        new Promise((res, rej) => {
            db()
                .collection('users')
                .find({ username: uname, password: pass })
                .toArray((err, users) => {
                    console.log(users)
                    err ? rej(err) : res(users.length > 0)
                })
        })
})

module.exports = factory(db)

module.exports.factory = factory
