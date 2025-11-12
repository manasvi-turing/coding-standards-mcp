require('dotenv').config();

const settings = {
  APP_NAME: process.env.APP_NAME || 'AI-SDLC-Express',
  VERSION: process.env.VERSION || '1.0.0',
  ENV: process.env.NODE_ENV || 'development',
  PORT: process.env.PORT || 3000,
  FASTAPI_BASE_URL: process.env.FASTAPI_BASE_URL || 'http://localhost:8000',
  CORS_ORIGIN: process.env.CORS_ORIGIN || 'http://localhost:3000',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
};

module.exports = { settings };

