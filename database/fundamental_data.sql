CREATE TABLE IF NOT EXISTS Stock_DB.fundamental_data (
  `ticker` VARCHAR(16) PRIMARY KEY,
  `city` text,
  `state` text,
  `zip` text,
  `country` text,
  `website` text,
  `sector` text,
  `open` double DEFAULT NULL,
  `dayLow` double DEFAULT NULL,
  `dayHigh` double DEFAULT NULL,
  `payoutRatio` double DEFAULT NULL,
  `beta` double DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `marketCap` bigint DEFAULT NULL,
  `currentPrice` double DEFAULT NULL,
  `targetHighPrice` double DEFAULT NULL,
  `totalCash` bigint DEFAULT NULL,
  CONSTRAINT fk_fundamental_data_tickers FOREIGN KEY (ticker) REFERENCES Stock_DB.tickers (symbol)
);


    