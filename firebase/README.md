# Firebase Functions Deployment

Firebase functions deploy from a node.js app (_I think_). This means that your
changes won't propagate unless you deploy them to the server.


## Usage

### File Structure

Firebase is split into separate parts, subsections of the directory deal with different services. Since we are only using functions this is the only directory.

```
firebase
├── README.md
├── firebase.json
├── package-lock.json
└── functions
    ├── index.js
    ├── node_modules
    ├── package-lock.json
    └── package.json

```

### Set Up

In order to deploy Firebase apps from your machine, you must first install the packages needed. From the `functions` directory do the following.

```
$ npm install
```

### Writing Functions

To write a function, add it to the index.js file.

**This is a bad solution! We need a better way to do this to prevent Git hell!!!**

### Enabling Deployment

In order to deploy your amazing functions you must first log in to Firebase.
```
$ firebase login
```
This will prompt you to enter your details. If you have not been given access to the project please contact Oktay. Once you have logged in, you will be able to deploy functions to Firebase.

**It is very important when deploying that you only deploy your function incase you have broken another!**
```
$ firebase deploy --only functions:<YOUR_FUNCTION>
```

Once finished, make sure to log out!

```
$ firebase logout
```
