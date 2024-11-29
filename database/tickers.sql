CREATE TABLE IF NOT EXISTS Stock_DB.tickers (
  symbol VARCHAR(16) PRIMARY KEY,
  name text,
  INDEX idx_tickers (symbol)
);