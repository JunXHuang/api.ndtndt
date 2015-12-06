CREATE TABLE Person (
    SSN VARCHAR(20),
    LastName VARCHAR(20) NOT NULL,
    FirstName VARCHAR(20) NOT NULL,
    Address VARCHAR(256),
    City VARCHAR(20),
    State VARCHAR(2),
    ZipCode INTEGER,
    Telephone VARCHAR(20),
    Email VARCHAR(100),
    UserPassword VARCHAR(36) NOT NULL,
    PersonImg VARCHAR(500),
    PRIMARY KEY (SSN))

CREATE TABLE Customer (
    Rating INTEGER,
    CreditCardNum VARCHAR(25),
    CustomerID VARCHAR(20),
    PRIMARY KEY (CustomerID),
    FOREIGN KEY (CustomerID) REFERENCES Person (SSN)
        ON DELETE CASCADE
        ON UPDATE CASCADE )
        
CREATE TABLE Employee (
    StartDate DATETIME,
    HourlyRate MONEY,
    MagLevel BIT NOT NULL,
    EmployeeID VARCHAR(20),
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES Person(SSN)
        ON DELETE CASCADE
        ON UPDATE CASCADE )

CREATE TABLE Item (
	ItemName VARCHAR(255),
    ItemType VARCHAR(50),
    YearManufactured INTEGER,
    CopiesSold INTEGER DEFAULT 0,
	AmountInStock INTEGER,
    PRIMARY KEY (ItemName),
	CHECK (YearManufactured>0 AND YearManufactured<9999))
    
CREATE TABLE Auction (
    AuctionID INTEGER IDENTITY(1,1),
    OpenBid MONEY,
    BidIncrement MONEY,
    ReservePrice MONEY DEFAULT 0,
    CurrentHighBid MONEY DEFAULT 0,
    currentBid MONEY DEFAULT 0,
    Monitor VARCHAR(20),
    ItemName VARCHAR(255) NOT NULL,
    Sold BIT DEFAULT 0,
    SellerID VARCHAR(20) NOT NULL,
    ItemImg VARCHAR(500),
    descriptions VARCHAR(1000),
    PRIMARY KEY (AuctionID),
    FOREIGN KEY (Monitor) REFERENCES Employee (EmployeeID)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY (ItemName) REFERENCES Item
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY (SellerID) REFERENCES Customer(CustomerID))

CREATE TABLE Post (
    ExpireDates DATETIME,
    PostDate DATETIME,
    CustomerID VARCHAR(20),
    AuctionID INTEGER NOT NULL,
    ItemName VARCHAR(255) NOT NULL,
    PRIMARY KEY (CustomerID, ItemName,AuctionID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY (ItemName) REFERENCES Item(ItemName),
    FOREIGN KEY (AuctionID) REFERENCES Auction(AuctionID))

CREATE TABLE Bid (
    BidKey INTEGER IDENTITY(1,1),
    CustomerID VARCHAR(20),
    AuctionID INTEGER,
    BidPrice MONEY,
    BidDate DATETIME,
    PRIMARY KEY (bidKey),
    FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(AuctionID) REFERENCES Auction(AuctionID))



ALTER TABLE Item
ADD CHECK(ItemType IN ('DVD', 'BOOK', 'CAR', 'BABY','TOYS','CLOTHING','JEWELRY','ELECTRONICS','SILVERWARE','SPORT','CLEANING'))


CREATE TABLE StaffPicks(
    AuctionID INTEGER,
    PRIMARY KEY (AuctionID),
    FOREIGN KEY (AuctionID) REFERENCES Auction
)
CREATE TABLE UserPicks(
    UserPicksID INTEGER IDENTITY(1,1), 
    AuctionID INTEGER,
    UserID VARCHAR(20),
    PRIMARY KEY (UserPicksID),
    FOREIGN KEY (AuctionID) REFERENCES Auction,
    FOREIGN KEY (UserID) REFERENCES Customer(customerid)
)

create table BiddingHistory(
    BiddingHistoryID INTEGER IDENTITY(1,1),
    AuctionID INTEGER,
    CurrentWinner VARCHAR(20),
    CurrentBid MONEY,
    CurrentHighBid MONEY,
    BidIncrement MONEY,
    BidPrice MONEY,
    Bidder VARCHAR(20),
    PRIMARY KEY (BiddingHistoryID),
    FOREIGN KEY (AuctionID) REFERENCES Auction,
    FOREIGN KEY (CurrentWinner) REFERENCES Person(ssn),
	FOREIGN KEY (bidder) references customer(customerid)
)
