const config = require('config');
const winston = require('winston');

const logger = winston.createLogger({
  level: config.get('logger.level'),
  format: format.combine(
    format.timestamp(),
    format.json()
  ),
  defaultMeta: { service: 'digital-paper-edit-infrastructure' },
  transports: [
    new winston.transports.File({
      filename: config.get('logger.error'),
      level: 'error'
    }),
    new winston.transports.File({
      filename: config.get('logger.file')
    })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new transports.Console({
    format: format.combine(
      format.colorize(),
      format.simple()
    )
  }));
}

module.exports = logger;
