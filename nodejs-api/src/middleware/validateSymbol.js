/**
 * Middleware to validate presence of `symbol` query param
 */
module.exports = (req, res, next) => {
  const symbol = req.query.symbol;
  if (!symbol || !symbol.trim()) {
    return res.status(400).json({
      status: 'error',
      message: 'Missing required parameter: symbol',
    });
  }
  req.symbol = symbol.trim().toUpperCase();
  next();
};

