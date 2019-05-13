const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

const logger = require('./logger');

const port = process.env.PORT || 8080;
const app = express();

app.use(bodyParser.json());

if (process.env.NODE_ENV === 'live') {
  const staticDirectory = path.join(__dirname, '..', 'static');

  app.use(express.static(staticDirectory));

  app.get('*', (req, res) => {
    res.sendFile(path.join(staticDirectory, 'index.html'));
  });
}

app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;

  res.status(statusCode).json({
    status: statusCode,
    message: err.message
  });
});

const server = app.listen(port, () => {
  logger.info(`listening on ${config.get('host')}:${port}`);
  logger.info(`Current NODE_ENV setting: ${process.env.NODE_ENV}`);
});

server.on('error', (err) => {
  logger.error(err);
});

require('./routes/index')(app);
require('./routes/status')(app);

module.exports = app;
