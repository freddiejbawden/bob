const app = require('./app')
const db = require('./db')
const bonjour = require('bonjour')()
const utils = require('./utils')
const fakeData = require('./fake_db.json')
const fs = require('fs')

const PORT = process.env.PORT || 9000
const FAKE_DATA = process.env.DATA === 'fake'

console.log('Using api level ' + app.API_LEVEL)

db.init()
    .then(async db => {
        console.log('Initialized database connection.')

        if (FAKE_DATA) {
            await db.dropDatabase()
            await utils.loadDBwithData(db, fakeData)
            console.log('Initialized database with fake data.')
        }

        app.get('/api/commit', (req, res) => {
            try {
                const commit = fs.readFileSync('./COMMIT', 'utf8').trim()
                res.redirect('https://github.com/Assis10t/assis10t/commit/' + commit)
            } catch (e) {
                res.status(404).send('This isnt a travis build, so commit id is unavailable.')
            }
        })

        app.get('/api/reset', async (req, res) => {
            await db.dropDatabase()
            if (FAKE_DATA) {
                await utils.loadDBwithData(db, fakeData)
                res.send('Deleted all data and reloaded with fake data.')
            } else {
                res.send('Deleted all data.')
            }
        })

        app.listen(PORT, () => {
            console.log(`Listening on port ${PORT}.`)
        })

        //assis10t._http._tcp.
        bonjour.publish({ name: 'assis10t', type: 'http', host: utils.getIp(), port: PORT })
    })
    .catch(err => console.error('Error initializing database connection.', err))
