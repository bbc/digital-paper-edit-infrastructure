module.exports = (app) => {
  app.get('/', (req, res) => {
    res.json({
      links: {
        status: ('127.0.0.1:8080/status'),
      },
    });
  });
};
