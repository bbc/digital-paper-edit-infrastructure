const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();

app.use(bodyParser.json());

if (process.env.NODE_ENV === 'live') {
  const staticIndex = path.join(
    __dirname,
    '/node_modules/@bbc',
    '/digital-paper-edit-client',
    '/index.html',
  );

  app.use(express.static(staticIndex));

}

app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;

  res.status(statusCode).json({
    status: statusCode,
    message: err.message,
  });
});

const server = app.listen(8080, () => {
  console.log('listening on 8080');
  console.log(`Current NODE_ENV setting: ${process.env.NODE_ENV}`);
});

server.on('error', (err) => {
  console.log(err);
});

module.exports = app;
