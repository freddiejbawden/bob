import * as firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/firestore'
import 'firebase/database'

var config = {
    apiKey: "AIzaSyCF2eBVyk_OX4Z9tWY_i5jRgM9xZghnUMQ",
    authDomain: "assis10t-524c5.firebaseapp.com",
    databaseURL: "https://assis10t-524c5.firebaseio.com",
    projectId: "assis10t-524c5",
    storageBucket: "assis10t-524c5.appspot.com",
    messagingSenderId: "652646052342"
};

!firebase.apps.length ? firebase.initializeApp(config) : ''
export const GoogleProvider = new firebase.auth.GoogleAuthProvider()
export const auth = firebase.auth()
export const DB = firebase.database()
export const StoreDB = firebase.firestore()
export default firebase