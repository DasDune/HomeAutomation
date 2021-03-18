const express =   
 require('express');
const app = express();
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb' }));
app.use('/res', express.static('res'));

const path = require('path');

const port = 8080;

// var admin = require('firebase-admin');
// var serviceAccount = require('./serviceAccountKey.json');
// admin.initializeApp({
//     credential: admin.credential.cert(serviceAccount),
//     databaseURL: "https://homeautomation-654d6.firebaseio.com"
//   });

const cors = require('cors');
app.use(cors());

const fs = require('fs');

// *** dependencies end ***

// Home page redirect Sign in page with auth scripts
app.get('/', (req, res) => {
    // res.send('Hello');
    res.sendFile(`${__dirname}/index.html`);
});