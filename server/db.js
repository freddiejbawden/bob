const MongoClient = require('mongodb').MongoClient
const MongoMemoryServer = require('mongodb-memory-server').MongoMemoryServer

const MEMORY_DB = process.env.DB === 'memory'
const MONGO_URL = process.env.MONGO || 'mongodb://localhost:27017/db'

let mongod = null
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
    if (MEMORY_DB) {
        mongod = new MongoMemoryServer()
        mongo_url = await mongod.getConnectionString()
        console.log('Using fake mongo at ' + mongo_url)
    } else {
        console.log('Using real mongo.')
    }
    client = new MongoClient(mongo_url, {
        useNewUrlParser: true
    })
    await client.connect()
    db = client.db('bob')

    return db
}

module.exports.close = () => {
    if (client) client.close()
    //if (db) db.close()
    if (mongod) mongod.stop()
}
