CREATE TABLE IF NOT EXISTS Stock_DB.portfolio (
  `ticker` VARCHAR(16) PRIMARY KEY,
  `name` text,
  CONSTRAINT fk_portfolio_tickers FOREIGN KEY (ticker) REFERENCES Stock_DB.tickers (symbol)
);