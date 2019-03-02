const request = require('supertest')
const app = require('../app')
const utils = require('../utils')
const ObjectID = require('mongodb').ObjectID
const db = require('../db')

// Disable logging.
beforeAll(() => (console.log = jest.fn()))

beforeEach(db.init)

afterEach(db.close)

describe('/register', () => {
    it('works', async () => {
        const response = await request(app)
            .post('/register')
            .send({
                username: 'myusername',
                type: 'customer'
            })
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            user: {
                username: 'myusername',
                type: 'customer'
            }
        })

        const _id = response.body.user._id

        expect(_id).toBeTruthy()

        const dbUser = await db()
            .collection('users')
            .findOne({ _id: ObjectID(_id) })

        expect(dbUser).toMatchObject({
            username: 'myusername',
            type: 'customer'
        })
    })
})
