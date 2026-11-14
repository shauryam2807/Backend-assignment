/**
 * Twelve Data Compatible Endpoints
 */
const express = require('express');
const router = express.Router();

const validateSymbol = require('../middleware/validateSymbol');
const priceController = require('../controllers/price.controller');
const timeseriesController = require('../controllers/timeseries.controller');
const quoteController = require('../controllers/quote.controller');
const exchangerateController = require('../controllers/exchangerate.controller');
const eodController = require('../controllers/eod.controller');

router.get('/price', validateSymbol, priceController.getPrice);
router.get('/time_series', validateSymbol, timeseriesController.getTimeSeries);
router.get('/quote', validateSymbol, quoteController.getQuote);
router.get('/exchange_rate', validateSymbol, exchangerateController.getExchangeRate);
router.get('/eod', validateSymbol, eodController.getEod);

module.exports = router;

