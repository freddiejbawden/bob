const request = require('supertest')
const app = require('../app')
const utils = require('../utils')
const ObjectID = require('mongodb').ObjectID
const db = require('../db')
const auth = require('../auth')

// Disable logging.
beforeAll(() => (console.log = jest.fn()))

beforeEach(db.init)

afterEach(db.close)

describe('GET /warehouse', () => {
    it.skip('works with 1 warehouse', async () => {
        const warehouse = {
            _id: '5c7e69bc0e604001687f860d',
            merchantId: '5c7e69d32fd94c017b8c5861',
            name: 'Example',
            image: 'some_image',
            location: {
                latitude: 1.24233,
                longitude: 2.12324
            },
            dimensions: {
                x: 2,
                y: 2,
                z: [0]
            }
        }
        utils.loadDBwithData(db(), {
            warehouses: [warehouse]
        })

        const response = await request(app).get('/warehouse')
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            warehouses: [warehouse]
        })
    })

    it.skip('works with no warehouses', async () => {
        const response = await request(app).get('/warehouse')
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            warehouses: []
        })
    })
})

describe('POST /warehouses', () => {
    it.skip('requires auth', async () => {
        const warehouse = {
            name: 'Example',
            image: 'some_image',
            location: {
                latitude: 1.24233,
                longitude: 2.12324
            },
            dimensions: {
                x: 2,
                y: 2,
                z: [0]
            }
        }

        const response = await request(app)
            .post('/warehouse')
            .send(warehouse)
        expect(response.statusCode).toBe(401)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('')
        })

        const newWarehouse = await db()
            .collection('warehouses')
            .findOne({})

        expect(newWarehouse).toBeNull()
    })

    it.skip('creates new warehouse', async () => {
        const merchantId = '5c7e69d32fd94c017b8c5861'
        utils.loadDBwithData(db(), {
            users: [
                {
                    _id: merchantId,
                    username: 'test',
                    type: 'merchant'
                }
            ]
        })

        const warehouse = {
            name: 'Example',
            image: 'some_image',
            location: {
                latitude: 1.24233,
                longitude: 2.12324
            },
            dimensions: {
                x: 2,
                y: 2,
                z: [0]
            }
        }

        const response = await request(app)
            .post('/warehouse')
            .set('username', 'test')
            .send(warehouse)
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            warehouse: { ...warehouse, merchantId }
        })

        const newWarehouse = await db()
            .collection('warehouses')
            .findOne({})

        expect(newWarehouse).toMatchObject(warehouse)
    })

    it.skip('edits existing warehouse', async () => {
        const merchantId = '5c7e69d32fd94c017b8c5861'

        const warehouse = {
            _id: '5c7e6dd6568c6708367e7f72',
            merchantId,
            name: 'Example',
            image: 'some_image',
            location: {
                latitude: 1.24233,
                longitude: 2.12324
            },
            dimensions: {
                x: 2,
                y: 2,
                z: [0]
            }
        }

        utils.loadDBwithData(db(), {
            users: [
                {
                    _id: merchantId,
                    username: 'test',
                    type: 'merchant'
                }
            ],
            warehouses: [warehouse]
        })

        const edit = {
            _id: warehouse._id,
            name: 'edited example',
            location: {
                latitude: 0.4,
                longitude: 0.6
            }
        }

        const response = await request(app)
            .post('/warehouse')
            .set('username', 'test')
            .send(edit)

        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            warehouse: { ...warehouse, ...edit }
        })

        const newWarehouse = await db()
            .collection('warehouses')
            .findOne({})

        expect(newWarehouse).toMatchObject({
            ...response.body.warehouse,
            _id: ObjectID(warehouse._id),
            merchantId: ObjectID(merchantId)
        })
    })

    it.skip('doesnt edit existing warehouse owned by someone else', async () => {
        const merchantId = '5c7e69d32fd94c017b8c5861'

        const warehouse = {
            _id: '5c7e6dd6568c6708367e7f72',
            merchantId,
            name: 'Example',
            image: 'some_image',
            location: {
                latitude: 1.24233,
                longitude: 2.12324
            },
            dimensions: {
                x: 2,
                y: 2,
                z: [0]
            }
        }

        utils.loadDBwithData(db(), {
            users: [
                {
                    _id: merchantId,
                    username: 'test',
                    type: 'merchant'
                },
                {
                    _id: '5c7e720ea56c73150e1108ae',
                    username: 'another_user',
                    type: 'merchant'
                }
            ],
            warehouses: [warehouse]
        })

        const edit = {
            _id: warehouse._id,
            name: 'edited example',
            location: {
                latitude: 0.4,
                longitude: 0.6
            }
        }

        const response = await request(app)
            .post('/warehouse')
            .set('username', 'another_user')
            .send(edit)

        expect(response.statusCode).toBe(403)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('permission')
        })
    })
})
