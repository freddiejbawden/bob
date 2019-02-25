# Bob Server

### Installation

```
npm install
```

### Starting the server
```
npm start
```

### Development
Instead of `npm start`, use:
```
npm run dev
```
This will restart the server whenever you change a file. It also creates and uses a fake mongodb instance in memory with data in `fake_db.json`. To use a real database, use `npm run dev-real` instead.

*Note: Please install the [Prettier Plugin](https://prettier.io/docs/en/editors.html) on your preferred text editor, and set it up to __format on save__. This will automatically format the code to be more readable.*

### Running tests
```
npm test
```

### Configuration
Change these environment variables before running the server:
```bash
PORT=9000                            # Port the server will run on.
MONGO=mongodb://localhost:27017/db   # URL of the mongo instance
DB=fake                              # Use fake in-memory mongodb instance with pre-defined data in fake_db.json. (Overrides MONGO=...)
```

## Documentation

### Auth
```javascript
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
```