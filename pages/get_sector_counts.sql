DELIMITER $$

CREATE PROCEDURE AnalyzeData()
BEGIN
    DECLARE avg_price FLOAT;
    DECLARE max_price FLOAT;

    SELECT AVG(currentPrice) INTO avg_price FROM fundamental_data;
    SELECT MAX(currentPrice) INTO max_price FROM fundamental_data;

    SELECT avg_price AS average_price, max_price AS maximum_price;

END$$

DELIMITER ;
