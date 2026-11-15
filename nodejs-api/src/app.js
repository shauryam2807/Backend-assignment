/**
 * Express Application Setup
 * Production-grade middleware stack with security, logging, and rate limiting.
 */
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const healthRoutes = require('./routes/health.routes');
const twelvedataRoutes = require('./routes/twelvedata.routes');
const referenceRoutes = require('./routes/reference.routes');
const legacyRoutes = require('./routes/legacy.routes');
const errorHandler = require('./middleware/errorHandler');
const { getDashboardHtml } = require('./views/dashboard.html');

const app = express();

// ---------------------------------------------------------------------------
// Security Middleware
// ---------------------------------------------------------------------------
app.use(helmet({ contentSecurityPolicy: false })); // Set secure headers, allow dashboard CDNs
app.use(cors());                             // Allow cross-origin requests

// ---------------------------------------------------------------------------
// Request Logging
// ---------------------------------------------------------------------------
const logFormat = process.env.NODE_ENV === 'production' ? 'combined' : 'dev';
app.use(morgan(logFormat));

// ---------------------------------------------------------------------------
// Rate Limiting (Protects API from spam while allowing smooth UI auto-refresh)
// ---------------------------------------------------------------------------
const maxRequests = process.env.NODE_ENV === 'production' ? 500 : 5000;
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: maxRequests,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    status: 'error',
    message: 'Too many requests from this IP, please try again after 15 minutes',
  },
});
app.use(limiter);

// ---------------------------------------------------------------------------
// Body Parsing
// ---------------------------------------------------------------------------
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ---------------------------------------------------------------------------
// Response Time Header
// ---------------------------------------------------------------------------
app.use((req, res, next) => {
  const start = process.hrtime();
  const originalJson = res.json.bind(res);
  res.json = (body) => {
    const [seconds, nanoseconds] = process.hrtime(start);
    const ms = (seconds * 1000 + nanoseconds / 1e6).toFixed(2);
    res.set('X-Response-Time', `${ms}ms`);
    return originalJson(body);
  };
  next();
});

// ---------------------------------------------------------------------------
// Root & UI Dashboard Endpoint
// ---------------------------------------------------------------------------
// Serves interactive Financial Trading Terminal UI when requested in a browser
// Serves JSON metadata when called by APIs, curl, or automated test runners
app.get('/', (req, res) => {
  if (req.headers.accept && req.headers.accept.includes('text/html')) {
    return res.send(getDashboardHtml());
  }
  res.json({
    name: 'MFAPIs Financial Data Platform (Node.js)',
    version: '2.0.0',
    documentation: '/health',
    dashboard: '/dashboard',
    description: 'Twelve Data Compatible Institutional Financial Data REST API',
    github: 'https://github.com/shauryam2807/Backend-assignment',
  });
});

app.get('/dashboard', (req, res) => {
  res.send(getDashboardHtml());
});

// ---------------------------------------------------------------------------
// Register API Routes
// ---------------------------------------------------------------------------
app.use('/', healthRoutes);
app.use('/', twelvedataRoutes);
app.use('/', referenceRoutes);
app.use('/v1', legacyRoutes);

// ---------------------------------------------------------------------------
// 404 Handler
// ---------------------------------------------------------------------------
app.use((req, res) => {
  res.status(404).json({
    status: 'error',
    message: 'Endpoint not found',
    path: req.originalUrl,
  });
});

// ---------------------------------------------------------------------------
// Global Error Handler
// ---------------------------------------------------------------------------
app.use(errorHandler);

module.exports = app;
