const request = require('supertest')
const app = require('../app')
const utils = require('../utils')
const db = require('../db')

// Disable logging.
beforeAll(() => (console.log = jest.fn()))

beforeEach(db.init)

afterEach(db.close)

describe('/ping', () => {
    it('works', async () => {
        const response = await request(app).get('/ping')
        expect(response.statusCode).toBe(200)
        expect(response.text).toEqual('pong')
    })
})
