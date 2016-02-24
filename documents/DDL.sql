CREATE USER 'wienwahl'@'%' IDENTIFIED BY 'wienwahl';
GRANT ALL PRIVILEGES ON wienwahl TO 'wienwahl'@'%';

DROP DATABASE IF EXISTS wienwahl;
CREATE DATABASE wienwahl;
USE wienwahl;
s
CREATE TABLE Wahlkreis (
	wahlkreisnr INT,
	wahlkreisname VARCHAR(100),
	
	PRIMARY KEY (wahlkreisnr)
);

CREATE TABLE Bezirk (
	bezirknr INT,
	bezirkname VARCHAR(100),
	wahlkreisnr INT,
	
	PRIMARY KEY (bezirknr),
	FOREIGN KEY (wahlkreisnr) REFERENCES Wahlkreis(wahlkreisnr)
);

CREATE TABLE Partei (
	parteiname VARCHAR(100),
	bez_lang VARCHAR(100),
	
	PRIMARY KEY (parteiname)
);

CREATE TABLE Wahl (
	wahltermin DATE,
	mandate INT,
	
	PRIMARY KEY (wahltermin)
);

CREATE TABLE Sprengel (
	sprengelnr INT,
	bezirknr INT,
	wahltermin DATE,
	wahlberechtigte INT,
	abgeg_stimmen INT,
	ung_stimmen INT,
	
	PRIMARY KEY (sprengelnr, bezirknr, wahltermin),
	FOREIGN KEY (bezirknr) REFERENCES Bezirk(bezirknr),
	FOREIGN KEY (wahltermin) REFERENCES Wahl(wahltermin)
);

CREATE TABLE Parteistimmen (
	parteiname VARCHAR(100),
	sprengelnr INT,
	bezirknr INT,
	wahltermin DATE,
	menge INT,
	
	PRIMARY KEY (parteiname, sprengelnr, bezirknr, wahltermin),
	FOREIGN KEY (bezirknr) REFERENCES Sprengel(bezirknr),
	FOREIGN KEY (wahltermin) REFERENCES Sprengel(wahltermin),
	FOREIGN KEY (sprengelnr) REFERENCES Sprengel(sprengelnr),
	FOREIGN KEY (parteiname) REFERENCES Partei(parteiname)
);

CREATE TABLE Kandidatur (
	wahlkreisnr INT,
	wahltermin DATE,
	parteiname VARCHAR(100),
	listenplatz INT,
	
	PRIMARY KEY (wahlkreisnr, wahltermin, parteiname),
	FOREIGN KEY (parteiname) REFERENCES Partei(parteiname),
	FOREIGN KEY (wahltermin) REFERENCES Wahl(wahltermin),
	FOREIGN KEY (wahlkreisnr) REFERENCES Wahlkreis(wahlkreisnr)
);

INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (1, 'Zentrum');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (2, 'Innen-West');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (3, 'Leopoldstadt');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (4, 'Landstraße');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (5, 'Favoriten');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (6, 'Simmering');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (7, 'Meidling');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (8, 'Hietzing');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (9, 'Penzing');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (10, 'Rudolfsheim-Fünfhaus');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (11, 'Ottakring');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (12, 'Hernals');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (13, 'Währing');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (14, 'Döbling');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (15, 'Brigittenau');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (16, 'Floridsdorf');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (17, 'Donaustadt');
INSERT INTO wahlkreis (wahlkreisnr, wahlkreisname) VALUES (18, 'Liesing');

INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (1, 'Innere Stadt', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (2, 'Leopoldstadt', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (3, 'Landstraße', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (4, 'Wieden', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (5, 'Margareten', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (6, 'Mariahilf', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (7, 'Neubau', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (8, 'Josefstadt', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (9, 'Alsergrund', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (10, 'Favoriten', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (11, 'Simmering', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (12, 'Meidling', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (13, 'Hietzing', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (14, 'Penzing', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (15, 'Rudolfsheim-Fünfhaus', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (16, 'Ottakring', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (17, 'Hernals', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (18, 'Währing', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (19, 'Döbling', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (20, 'Brigittenau', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (21, 'Floridsdorf', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (22, 'Donaustadt', 1);
INSERT INTO bezirk (bezirknr, bezirkname, wahlkreisnr) VALUES (23, 'Liesing', 1);

INSERT INTO Partei (parteiname, bez_lang) VALUES ('SPOE', 'Sozialdemokratische Partei Österreichs');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('FPOE', 'Freiheitliche Partei Österreichs');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('OEVP', 'Österreichische Volkspartei');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('GRUE', 'Grüne Partei Österreichs');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('NEOS', 'Das Neue Österreich und Liberales Forum');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('WWW', 'Wir wollen Wahlfreiheit');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('ANDAS', 'Wien anders');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('GFW', 'Gemeinsam für Wien');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('SLP', 'Sozialistische LinksPartei');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('WIFF', 'Wir für Floridsdorf');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('M', 'Männerpartei');
INSERT INTO Partei (parteiname, bez_lang) VALUES ('FREIE', 'Freidemokraten');

INSERT INTO Wahl (wahltermin, mandate) VALUES ('2015-09-11', 100);

INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 1, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 2, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 3, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 4, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 5, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 6, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 7, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 8, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 9, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 10, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 11, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 12, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 13, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 14, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 15, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 16, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 17, 'SPOE', 1);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 18, 'SPOE', 1);

INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 1, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 2, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 3, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 4, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 5, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 6, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 7, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 8, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 9, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 11, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 12, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 13, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 14, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 15, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 16, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 17, 'FPOE', 2);
INSERT INTO Kandidatur (wahltermin, wahlkreisnr, parteiname, listenplatz) VALUES ('2015-09-11', 18, 'FPOE', 2);



