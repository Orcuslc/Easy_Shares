DROP TABLE IF EXISTS stock_basics;
CREATE TABLE stock_basics (
	code INTEGER NOT NULL PRIMARY KEY,
	name STRING NOT NULL,
	holdingQuantity INTEGER NOT NULL	
);
CREATE TABLE stock_concept (
	code INTEGER NOT NULL PRIMARY KEY,
	c_name STRING NOT NULL,
	FOREIGN KEY(code) REFERENCES stock_basics(code)
);
CREATE TABLE stock_price (
	code INTEGER NOT NULL,
	date STRING NOT NULL,
	close REAL,
	price_change REAL,
	PRIMARY KEY(code, date),
	FOREIGN KEY(code) REFERENCES stock_basics(code)
);

INSERT INTO stock_basics
	VALUES(1, 'szzs', 0),
		  (603800, 'dsgf', 0);

INSERT INTO stock_concept
	VALUES(1, 'dp'),
		  (603800, 'tr');

INSERT INTO stock_price
	VALUES(1, '2015-12-02', 3552.34, 0.44),
		  (603800, '2015-12-02', 10.95, 0);