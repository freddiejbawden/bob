const MongoClient = require('mongodb').MongoClient
const MongoMemoryServer = require('mongodb-memory-server').MongoMemoryServer
const FAKE_DB = process.env.DB === 'fake'
const MONGO_URL = process.env.MONGO || 'mongodb://localhost:27017/db'
const fakeData = require('./fake_db.json')
const loadDBwithData = require('./utils').loadDBwithData

let client = null
let db = null

module.exports = () => {
    if (!client || !db) {
        throw new Error('Database connection has not been initialized.')
    }
    return db
}

module.exports.init = async () => {
    let mongo_url = MONGO_URL
    if (FAKE_DB) {
        const mongod = new MongoMemoryServer()
        mongo_url = await mongod.getConnectionString()
        console.log('Using fake mongo at ' + mongo_url)
    } else {
        console.log('Using real mongo at ' + mongo_url)
    }
    client = new MongoClient(mongo_url, {
        useNewUrlParser: true
    })
    await client.connect()
    db = client.db('bob')

    if (FAKE_DB) {
        await loadDBwithData(db, fakeData)
        console.log('Initialized database with fake data.')
    }
    return db
}
