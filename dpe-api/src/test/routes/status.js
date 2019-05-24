'use strict';

const server = require('../..');
const request = require('supertest');

describe('GET /', () => {
  it('returns a 200 status', (done) => {
    request(server)
      .get('/')
      .expect(200, done);
  });
});
