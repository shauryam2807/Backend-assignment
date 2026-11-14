/**
 * Controller for Legacy MFAPIs sample endpoints
 */
const ForexRate = require('../models/forexRate.model');
const CryptoPrice = require('../models/cryptoPrice.model');
const Economic = require('../models/economic.model');

exports.getForexSample = async (req, res, next) => {
  try {
    const data = await ForexRate.getSampleRates(25);
    res.json({
      status: 'success',
      meta: {
        source: 'frankfurter',
        sample_size: data.length,
        category: 'forex',
      },
      data,
    });
  } catch (err) {
    next(err);
  }
};

exports.getCryptoSample = async (req, res, next) => {
  try {
    const data = await CryptoPrice.getSamplePrices(25);
    res.json({
      status: 'success',
      meta: {
        source: 'coingecko',
        sample_size: data.length,
        category: 'cryptocurrency',
      },
      data,
    });
  } catch (err) {
    next(err);
  }
};

exports.getEconomicSample = async (req, res, next) => {
  try {
    const data = await Economic.getSampleValues(25);
    res.json({
      status: 'success',
      meta: {
        source: 'fred',
        sample_size: data.length,
        category: 'macroeconomic',
      },
      data,
    });
  } catch (err) {
    next(err);
  }
};

