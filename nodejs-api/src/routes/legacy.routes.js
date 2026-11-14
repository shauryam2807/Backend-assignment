/**
 * Legacy MFAPIs Sample Routes
 */
const express = require('express');
const router = express.Router();
const legacyController = require('../controllers/legacy.controller');

router.get('/forex/sample', legacyController.getForexSample);
router.get('/crypto/sample', legacyController.getCryptoSample);
router.get('/economic/sample', legacyController.getEconomicSample);

module.exports = router;

