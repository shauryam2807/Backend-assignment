/**
 * Reference Data Routes (/cryptocurrencies, /forex_pairs)
 */
const express = require('express');
const router = express.Router();
const referenceController = require('../controllers/reference.controller');

router.get('/cryptocurrencies', referenceController.getCryptocurrencies);
router.get('/forex_pairs', referenceController.getForexPairs);

module.exports = router;

