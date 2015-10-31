-- SQL Script to initialize the tables

DROP TABLE IF EXISTS pnames;
DROP TABLE IF EXISTS drecords;
DROP TABLE IF EXISTS pdates;

CREATE TABLE IF NOT EXISTS pnames(
	pname TEXT NOT NULL,
	CONSTRAINT cpk_pnames_pname PRIMARY KEY (pname)
);

CREATE TABLE IF NOT EXISTS drecords(
	pdate DATE NOT NULL,
	pname TEXT NOT NULL,
	CONSTRAINT cpk_drecords_pname PRIMARY KEY (pname),
	CONSTRAINT cfk_drecords_pdate FOREIGN KEY (pdate) REFERENCES pdates(pdate),
	CONSTRAINT cfk_drecords_pname FOREIGN KEY (pname) REFERENCES pnames(pname)
);

CREATE TABLE IF NOT EXISTS pdates(
	pdate DATE NOT NULL,
	CONSTRAINT cpk_pdates_pdate PRIMARY KEY (pdate)
);