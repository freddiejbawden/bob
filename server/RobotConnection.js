const realNet = require('net')

const robotConnectionFactory = net =>
    class RobotConnection {
        constructor() {
            this._onConnectedListeners = []
            this._onDataListeners = []
            this._server = null
            this.isConnected = false
        }

        start() {
            this._server = net.createServer(socket => {
                this.isConnected = true
                this._onConnectedListeners.forEach(listener => listener())

                socket.on('data', data => {
                    this._onDataListeners.forEach(listener =>
                        listener(data.toString())
                    )
                    //TODO: Parse the data before notifying listener.
                })

                socket.on('end', () => {
                    this.isConnected = false
                    console.log('Client disconnected.')
                })
            })

            this._server.listen(8000, () => {
                console.log('Server is listening.')
            })
        }

        stop() {
            this._server.close(() => {
                this._server = null
            })
        }

        isActive() {
            return !!this._server
        }

        onConnected(listener) {
            this._onConnectedListeners.push(listener)
            if (this.isConnected) {
                listener()
            }
        }

        onData(listener) {
            this._onDataListeners.push(listener)
        }
    }

module.exports = robotConnectionFactory(realNet)

module.exports.factory = robotConnectionFactory
