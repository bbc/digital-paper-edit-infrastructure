'use strict';

module.exports = (app) => {
  app.get('/status', (req, res) => {
    res.sendStatus(200);
  });
};
