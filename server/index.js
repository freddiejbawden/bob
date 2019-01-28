const RobotConnection = require('./RobotConnection')

const connection = new RobotConnection()
connection.start()
connection.onData(data => {
    console.log(data)
})
