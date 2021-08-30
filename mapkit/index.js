const dotenv = require('dotenv');
const express = require('express');
const jwt = require('jsonwebtoken');
const cellid = require('./lite.json');
// const https = require('https');

// Code added
const fs = require('fs')
let data = []
var arrOfJson = eval(fs.readFileSync('./lite.json','utf8'))

arrOfJson.map(e=>{
  data.push({
    "lon" : e['lat'],
    "lat" : e['lon'],
    "radio" : e['radio'],
    "cell" : e['cell']
  })
})

console.log(data)


//Code ended

dotenv.config();
const app = express();
// const options = {
//   key: fs.readFileSync('/keys/agent2-key.pem'),
//   cert: fs.readFileSync('/keys/agent2-cert.pem')
// };
const {
  AUTH_KEY,
  APPLE_TEAM_ID,
  MAPKIT_KEY_ID,
  PORT,
} = process.env;
const header = {
  kid: MAPKIT_KEY_ID, /* Key Id: Your MapKit JS Key ID */
  typ: 'JWT', /* Type of token */
  alg: 'ES256', /* The hashing algorithm being used */
};

app.use(express.static('public'));

app.get('/',function(req, res, next) {
  res.render(__dirname + "public/index.html");
})

app.get('/json',function(req, res, next) {
  res.json(data);
})

app.get('/token', (req, res, next) => {
  res.header('Cache-Control', 'no-cache, no-store, must-revalidate');
  next();
}, (req, res) => {
  const payload = {
    iss: APPLE_TEAM_ID, /* Issuer: Your Apple Developer Team ID */
    iat: Date.now() / 1000, /* Issued at: Current time in seconds */
    exp: (Date.now() / 1000) + 1800, /* Expire at: Time to expire the token */
  };

  res.send(jwt.sign(payload, AUTH_KEY, { header }));
});

app.listen(PORT, '0.0.0.0', () => {
  // eslint-disable-next-line no-console
  console.log(`Server started on port ${PORT}`);
  // console.log(`Server started on port ${ADDRESS}`);
});
