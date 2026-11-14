/**
 * Global Error Handling Middleware
 * Provides structured error responses with optional stack traces in development.
 */
module.exports = (err, req, res, _next) => {
  console.error(`[Error] ${req.method} ${req.originalUrl}:`, err.message);
  if (process.env.NODE_ENV === 'development') {
    console.error(err.stack);
  }

  const status = err.status || 500;
  const message = status === 500 ? 'Internal Server Error' : err.message;

  res.status(status).json({
    status: 'error',
    code: status,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};
