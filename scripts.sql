sqlite3 metrodensity.db 

PRAGMA foreign_keys = ON;
.headers ON
.mode column


CREATE TABLE IF NOT EXISTS lines (
  LineId INTEGER,
  LineName TEXT NOT NULL,
  DirectionId INTEGER PRIMARY KEY,
  DirectionName TEXT UNIQUE,
  DirectionValue INTEGER CHECK (DirectionValue IN (0,1))
);

INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (9, 'M1A', 66, 'Atatürk Havalimanı->Yenikapı', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (9, 'M1A', 67, 'Yenikapı->Atatürk Havalimanı', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (10, 'M1B', 30, 'Kirazlı->Yenikapı', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (10, 'M1B', 31, 'Yenikapı->Kirazlı', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (1, 'M2', 34, 'Yenikapı->Hacıosman', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (1, 'M2', 35, 'Hacıosman->Yenikapı', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (1, 'M2', 19, 'Sanayi Mahallesi->Seyrantepe', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (1, 'M2', 20, 'Seyrantepe->Sanayi Mahallesi', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (2, 'M3', 90, 'Bakırköy Sahil->Kayaşehir-Merkez', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (2, 'M3', 91, 'Kayaşehir-Merkez->Bakırköy Sahil', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (17, 'M9', 107, 'Ataköy->Olimpiyat', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (17, 'M9', 106, 'Olimpiyat->Ataköy', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (3, 'M4', 71, 'Sabiha Gökçen->Kadıköy', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (3, 'M4', 70, 'Kadıköy->Sabiha Gökçen', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (5, 'M5', 103, 'Samandıra->Üsküdar', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (5, 'M5', 102, 'Üsküdar->Samandıra', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (6, 'M6', 15, 'Levent->Hisarüstü-Boğaziçi Üniversitesi', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (6, 'M6', 16, 'Hisarüstü-Boğaziçi Üniversitesi->Levent', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (11, 'T1', 21, 'Bağcılar->Kabataş', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (11, 'T1', 22, 'Kabataş->Bağcılar', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (11, 'T1', 26, 'Cevizlibağ->Eminönü', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (11, 'T1', 27, 'Eminönü->Cevizlibağ', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (12, 'T3', 23, 'İskele Cami->Kadıköy İDO', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (13, 'T4', 17, 'Mescid-i Selam->Topkapı', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (13, 'T4', 18, 'Topkapı->Mescid-i Selam', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (14, 'T5', 86, 'Eminönü->Alibeyköy Cep Otogarı', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (14, 'T5', 87, 'Alibeyköy Cep Otogarı->Eminönü', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (4, 'F1', 13, 'Kabataş->Taksim', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (4, 'F1', 14, 'Taksim->Kabataş', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (20, 'F4', 72, 'Aşiyan->Rumeli Hisarüstü', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (20, 'F4', 73, 'Rumeli Hisarüstü->Aşiyan', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (15, 'TF1', 46, 'Maçka->Taşkışla', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (15, 'TF1', 47, 'Taşkışla->Maçka', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (16, 'TF2', 44, 'Eyüp->Piyerloti', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (16, 'TF2', 45, 'Piyerloti->Eyüp', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (7, 'M7', 42, 'Mecidiyeköy->Mahmutbey', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (7, 'M7', 43, 'Mahmutbey->Mecidiyeköy', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (7, 'M7', 74, 'Yıldız->Mecidiyeköy', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (7, 'M7', 75, 'Mecidiyeköy ->Yıldız', 0);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (8, 'M8', 78, 'Bostancı->Parseller', 1);
INSERT INTO lines (LineId, LineName, DirectionId, DirectionName, DirectionValue) VALUES (8, 'M8', 79, 'Parseller ->Bostancı', 0);


CREATE TABLE IF NOT EXISTS transferLine(
Id INTEGER PRIMARY KEY, 
LineName TEXT , 
From_where  TEXT, 
To_where TEXT
);

.mode csv
.import transferline.csv transferLine 

CREATE TABLE IF NOT EXISTS stations(
Id INTEGER PRIMARY KEY,
LineName TEXT , 
StationName  TEXT, 
DistirctName TEXT,
StationSize INTEGER,
Escalator_Cnt INTEGER,
Elevator_Cnt INTEGER
);

.import informationofstation.csv stations;


CREATE TABLE IF NOT EXISTS passenger_flow (
    FlowId INTEGER PRIMARY KEY AUTOINCREMENT,
    StationId INTEGER,
    LineId INTEGER,
    PassengerCount INTEGER,
    TransitionDate TEXT,
    TransitionHour INTEGER,
    FOREIGN KEY (StationId) REFERENCES stations(Id),
    FOREIGN KEY (LineId) REFERENCES lines(LineId)
);

CREATE TABLE IF NOT EXISTS Calendar (
    Date TEXT PRIMARY KEY,
    DayName TEXT,
    IsWorkDay INTEGER, 
    IsSpecialEvent INTEGER
);

CREATE TABLE IF NOT EXISTS Crowd_Thresholds (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    StationId INTEGER,
    UpperLimit INTEGER, 
    StatusLevel TEXT,   
    FOREIGN KEY (StationId) REFERENCES stations(Id)
);

CREATE TABLE IF NOT EXISTS Facilities (
    FacilityId INTEGER PRIMARY KEY AUTOINCREMENT,
    StationId INTEGER,
    FacilityType TEXT, 
    Status INTEGER,     
    FOREIGN KEY (StationId) REFERENCES stations(Id)
);

CREATE TABLE IF NOT EXISTS Search_Analytics (
    SearchId INTEGER PRIMARY KEY AUTOINCREMENT,
    SearchedStationId INTEGER,
    SearchCount INTEGER,
    SearchDate TEXT,
    FOREIGN KEY (SearchedStationId) REFERENCES stations(Id)
);

CREATE TABLE IF NOT EXISTS Line_Stations (
    LineId INTEGER,
    StationId INTEGER,
    StationOrder INTEGER, 
    PRIMARY KEY (LineId, StationId),
    FOREIGN KEY (LineId) REFERENCES lines(LineId),
    FOREIGN KEY (StationId) REFERENCES stations(Id)
);