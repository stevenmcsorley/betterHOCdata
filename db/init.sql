CREATE DATABASE IF NOT EXISTS members_data;

USE members_data;

CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL UNIQUE,
    nameListAs VARCHAR(255),
    nameDisplayAs VARCHAR(255),
    nameFullTitle VARCHAR(255),
    nameAddressAs VARCHAR(255),
    latestPartyId INT,
    latestPartyName VARCHAR(255),
    latestPartyAbbreviation VARCHAR(255),
    latestPartyBackgroundColour VARCHAR(255),
    latestPartyForegroundColour VARCHAR(255),
    latestPartyIsLordsMainParty BOOLEAN,
    latestPartyIsLordsSpiritualParty BOOLEAN,
    latestPartyGovernmentType INT,
    latestPartyIsIndependentParty BOOLEAN,
    gender CHAR(1),
    membershipFrom VARCHAR(255),
    membershipFromId INT,
    house INT,
    membershipStartDate DATETIME,
    membershipEndDate DATETIME,
    membershipEndReason VARCHAR(255),
    membershipEndReasonNotes VARCHAR(255),
    membershipEndReasonId INT,
    membershipStatusIsActive BOOLEAN,
    membershipStatusDescription VARCHAR(255),
    membershipStatusNotes VARCHAR(255),
    membershipStatusId INT,
    membershipStatus INT,
    membershipStatusStartDate DATETIME,
    thumbnailUrl VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS member_votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    house INT,
    division_id INT,
    in_affirmative_lobby BOOLEAN,
    acted_as_teller BOOLEAN,
    title VARCHAR(255),
    date DATE,
    division_number INT,
    number_in_favour INT,
    number_against INT
);

CREATE TABLE membervoting (
    member_id INT,
    division_id INT,
    date DATETIME,
    title VARCHAR(255),
    member_voted_aye BOOLEAN,
    member_was_teller BOOLEAN,
    PRIMARY KEY (member_id, division_id)
);