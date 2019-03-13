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

describe('POST /api/register', () => {
    it('works', async () => {
        const response = await request(app)
            .post('/api/register')
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

describe('POST /api/login', () => {
    it('retrieves the existing user', async () => {
        utils.loadDBwithData(db(), {
            users: [
                {
                    _id: '5c7a4a6bdd5efa0ef0916e1b',
                    username: 'test',
                    type: 'merchant'
                }
            ]
        })
        const response = await request(app)
            .post('/api/login')
            .send({
                username: 'test'
            })
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject({
            success: true,
            user: {
                _id: '5c7a4a6bdd5efa0ef0916e1b',
                username: 'test',
                type: 'merchant'
            }
        })
    })

    it('gives appropriate error if user is not found', async () => {
        const response = await request(app)
            .post('/api/login')
            .send({
                username: 'test'
            })
        expect(response.statusCode).toBe(401)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('incorrect')
        })
    })
})

describe('Auth Library', () => {
    it('works', async () => {
        const user = {
            _id: '5c7a4a6bdd5efa0ef0916e1b',
            username: 'test',
            type: 'customer'
        }
        utils.loadDBwithData(db(), {
            users: [user]
        })
        app.get('/api/__test__/auth/works', auth.customer((req, res) => res.json(req.user)))

        const response = await request(app)
            .get('/api/__test__/auth/works')
            .set('username', 'test')
        expect(response.statusCode).toBe(200)
        expect(response.body).toMatchObject(user)
    })

    it('rejects requests without username header', async () => {
        app.get('/api/__test__/auth/rejectsWithoutUsername', auth.customer((req, res) => res.json(req.user)))

        const response = await request(app).get('/api/__test__/auth/rejectsWithoutUsername')

        expect(response.statusCode).toBe(401)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('requires auth')
        })
    })

    it('rejects unknown users', async () => {
        app.get('/api/__test__/auth/rejectsUnknownUsers', auth.customer((req, res) => res.json(req.user)))

        const response = await request(app)
            .get('/api/__test__/auth/rejectsUnknownUsers')
            .set('username', 'test')

        expect(response.statusCode).toBe(401)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('not found')
        })
    })

    it('rejects users with incorrect type', async () => {
        const user = {
            _id: '5c7a4a6bdd5efa0ef0916e1b',
            username: 'test',
            type: 'merchant'
        }
        utils.loadDBwithData(db(), {
            users: [user]
        })
        app.get('/api/__test__/auth/rejectsIncorrectType', auth.customer((req, res) => res.json(req.user)))

        const response = await request(app)
            .get('/api/__test__/auth/rejectsIncorrectType')
            .set('username', 'test')

        expect(response.statusCode).toBe(403)
        expect(response.body).toMatchObject({
            success: false,
            error: expect.stringContaining('permission')
        })
    })
})
