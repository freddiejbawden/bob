const factory = require('./RobotConnection').factory
const net = require('net')

jest.mock('net')

let fakeSocket
let fakeServer

beforeEach(() => {
    // Returns a mock server that connects immediately to a fake socket.
    net.createServer.mockImplementation(onConnected => {
        fakeSocket = { on: jest.fn() }
        onConnected(fakeSocket)
        fakeServer = {
            listen: jest.fn(),
            close: jest.fn(listener => listener())
        }
        return fakeServer
    })
})

it('notifies onConnected listeners when it connects', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()

    const myOnConnected = jest.fn()
    connection.onConnected(myOnConnected)
    expect(myOnConnected.mock.calls.length).toBe(0)
    connection.start()
    expect(myOnConnected.mock.calls.length).toBe(1)
})

it('notifies new onConnected listeners if its already connected', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()

    connection.start()

    const myOnConnected = jest.fn()
    connection.onConnected(myOnConnected)
    expect(myOnConnected.mock.calls.length).toBe(1)
})

it('notifies onData listeners when new data arrives', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()

    const myOnData = jest.fn()
    connection.onData(myOnData)

    connection.start()

    fakeSocket.on.mock.calls.forEach(call => {
        if (call[0] === 'data') {
            const listener = call[1]
            listener('fakedata')
            expect(myOnData.mock.calls.length).toBe(1)
            expect(myOnData.mock.calls[0][0]).toEqual('fakedata')
        }
    })

    expect.assertions(2)
})

it('isConnected shows the status of the connection correctly', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()

    expect(connection.isConnected).toBe(false)
    connection.start()
    expect(connection.isConnected).toBe(true)

    fakeSocket.on.mock.calls.forEach(call => {
        if (call[0] === 'end') {
            const listener = call[1]
            listener()
            expect(connection.isConnected).toBe(false)
        }
    })

    expect.assertions(3)
})

it('can stop the server when stop() is called', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()
    connection.start()
    connection.stop()
    expect(fakeServer.close.mock.calls.length).toBe(1)
})

it('isActive shows the status of the server correctly', () => {
    const RobotConnection = factory(net)
    const connection = new RobotConnection()
    expect(connection.isActive()).toBe(false)
    connection.start()
    expect(connection.isActive()).toBe(true)
    connection.stop()
    expect(connection.isActive()).toBe(false)
})
