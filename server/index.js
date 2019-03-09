const app = require('./app')
const db = require('./db')
const bonjour = require('bonjour')()
const utils = require('./utils')
const fakeData = require('./fake_db.json')

const PORT = process.env.PORT || 9000
const FAKE_DB = process.env.DB === 'fake'

console.log('Using api level ' + app.API_LEVEL)

db.init()
    .then(async db => {
        console.log('Initialized database connection.')

        if (FAKE_DB) {
            await utils.loadDBwithData(db, fakeData)
            console.log('Initialized database with fake data.')
        }

        app.get('/commit', (req, res) => {
            if (process.env.TRAVIS_COMMIT) {
                res.redirect('https://github.com/Assis10t/assis10t/commit/' + process.env.TRAVIS_COMMIT)
            } else {
                res.status(404).send('This isnt a travis build, so commit id is unavailable.')
            }
        })

        app.listen(PORT, () => {
            console.log(`Listening on port ${PORT}.`)
        })

        //assis10t._http._tcp.
        bonjour.publish({ name: 'assis10t', type: 'http', host: utils.getIp(), port: PORT })
    })
    .catch(err => console.error('Error initializing database connection.', err))
