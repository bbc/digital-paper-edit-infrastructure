'use strict';

const config = require('config');
const dependency = require('../package');

const path = config.get('host');

module.exports = (app) => {
  app.get('/', (req, res) => {
    res.json({
      name: dependency.name,
      description: dependency.description,
      links: {
        status: (`${path}/status`)
      }
    });
  });
};
