'use strict';

const dependency = require('../package');

module.exports = (app) => {
  app.get('/', (req, res) => {
    res.json({
      name: dependency.name,
      description: dependency.description,
      links: {
              status: (`127.0.0.1:8080/status`)
      }
    });
  });
};
