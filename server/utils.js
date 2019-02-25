const os = require('os')
const ObjectID = require('mongodb').ObjectID

let ips = null

module.exports.getIp = () => {
    if (ips && ips.length > 0) return ips[0]

    ips = []
    const ifaces = os.networkInterfaces()
    console.log('===== IP ADDRESSES =====')
    Object.keys(ifaces).forEach(function(ifname) {
        let alias = 0

        ifaces[ifname].forEach(function(iface) {
            if ('IPv4' !== iface.family || iface.internal !== false) {
                // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
                return
            }

            ips.push(iface.address)

            if (alias >= 1) {
                // this single interface has multiple ipv4 addresses
                console.log(ifname + ':' + alias, iface.address)
            } else {
                // this interface has only one ipv4 adress
                console.log(ifname, iface.address)
            }
            ++alias
        })
    })
    console.log('=== END IP ADDRESSES ===')
    return ips[0]
}

module.exports.loadDBwithData = (db, data) => {
    const promises = Object.keys(data)
        .map(collection => ({
            collection,
            data: data[collection].map(doc => ({
                ...doc,
                _id: doc._id ? ObjectID(doc._id) : new ObjectID()
            }))
        }))
        .map(({ collection, data }) => db.collection(collection).insertMany(data))
    return Promise.all(promises)
}
