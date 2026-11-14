/**
 * Controller for Reference Data Endpoints
 */

exports.getCryptocurrencies = (req, res) => {
  res.json({
    data: [
      { symbol: 'BTC/USD', name: 'Bitcoin', currency_base: 'Bitcoin', currency_quote: 'US Dollar' },
      { symbol: 'ETH/USD', name: 'Ethereum', currency_base: 'Ethereum', currency_quote: 'US Dollar' },
      { symbol: 'BNB/USD', name: 'BNB', currency_base: 'BNB', currency_quote: 'US Dollar' },
      { symbol: 'SOL/USD', name: 'Solana', currency_base: 'Solana', currency_quote: 'US Dollar' },
      { symbol: 'XRP/USD', name: 'XRP', currency_base: 'XRP', currency_quote: 'US Dollar' },
    ],
    status: 'ok',
  });
};

exports.getForexPairs = (req, res) => {
  res.json({
    data: [
      { symbol: 'EUR/USD', currency_base: 'EUR', currency_quote: 'USD' },
      { symbol: 'GBP/USD', currency_base: 'GBP', currency_quote: 'USD' },
      { symbol: 'USD/JPY', currency_base: 'USD', currency_quote: 'JPY' },
      { symbol: 'USD/INR', currency_base: 'USD', currency_quote: 'INR' },
      { symbol: 'USD/CAD', currency_base: 'USD', currency_quote: 'CAD' },
      { symbol: 'AUD/USD', currency_base: 'AUD', currency_quote: 'USD' },
      { symbol: 'USD/CHF', currency_base: 'USD', currency_quote: 'CHF' },
    ],
    status: 'ok',
  });
};

