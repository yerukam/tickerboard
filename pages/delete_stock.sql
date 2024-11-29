DELIMITER $$

CREATE PROCEDURE DeleteData(
    IN ticket_symbol VARCHAR(20),
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    DELETE FROM fundamental_data
    WHERE ticker = ticker_symbol
    AND date BETWEEN start_date AND end_date;
END$$

DELIMITER;