const model = require('./model')

/*

// Usage:

const auth = require('./auth')

// Without auth:
app.get((req, res) => {
    res.send('Hello world!')
})

// With auth (for any logged in user):
app.get(auth.any((req, res) => {
    const currentUser = req.user
    res.send('Hello ' + currentUser.username)
}))

// With auth (merchants only):
app.get(auth.merchant((req, res) => {
    const currentUser = req.user
    res.send('Hello ' + currentUser.username)
}))
// Note: You can also use: auth.customer and auth.robot in this way

// Select your own user groups:
app.get(auth(['merchant', 'robot'], (req, res) => {
    const currentUser = req.user
    res.send('Hello ' + currentUser.username)
}))

*/

const authFactory = model => (userTypes, routeHandler) => (req, res, next) => {
    const username = req.header('username')
    if (!username) {
        res.status(401).json({
            success: false,
            error: 'This resource requires authentication.'
        })
        return
    }
    model
        .authUser(username)
        .then(user => {
            if (!user) {
                res.status(401).json({
                    success: false,
                    error: 'User not found.'
                })
            } else if (!userTypes.contains(user.type)) {
                res.status(403).json({
                    success: false,
                    error: 'You do not have the required permissions to access this resource.'
                })
            } else {
                req.user = user
                routeHandler(req, res, next)
            }
        })
        .catch(next)
}

module.exports = authFactory(model)
module.exports.factory = authFactory
module.exports.any = routeHandler => authFactory(model)(['customer', 'merchant', 'robot'], routeHandler)
module.exports.customer = routeHandler => authFactory(model)(['customer'], routeHandler)
module.exports.merchant = routeHandler => authFactory(model)(['merchant'], routeHandler)
module.exports.robot = routeHandler => authFactory(model)(['robot'], routeHandler)
