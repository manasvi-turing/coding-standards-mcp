const morgan = require('morgan');
const { settings } = require('../config/settings');

/**
 * Request logger middleware
 * Logs incoming requests with timestamp and details
 */
function requestLogger(req, res, next) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  next();
}

/**
 * Morgan logger configuration
 * Returns configured morgan middleware based on environment
 */
function getMorganLogger() {
  if (settings.ENV === 'production') {
    return morgan('combined');
  }
  return morgan('dev');
}

module.exports = {
  requestLogger,
  getMorganLogger,
};

