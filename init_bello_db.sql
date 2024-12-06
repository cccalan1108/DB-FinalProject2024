-- Create database if not exists
SELECT 'CREATE DATABASE bello'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bello');
-- Create tables for Bello platform
SET client_encoding = 'UTF8';
-- Create USER table
CREATE TABLE "USER" (
    User_id BIGINT PRIMARY KEY,
    Account VARCHAR(15) NOT NULL UNIQUE,
    User_name VARCHAR(20) NOT NULL,
    User_nickname VARCHAR(20) NOT NULL,
    Password VARCHAR(15) NOT NULL,
    Nationality VARCHAR(20) NOT NULL,
    City VARCHAR(20),
    Phone VARCHAR(20) NOT NULL UNIQUE,
    Email VARCHAR(50) NOT NULL UNIQUE,
    Sex VARCHAR(10) NOT NULL,
    Birthday DATE NOT NULL,
    Register_time TIMESTAMP NOT NULL
);

-- Create USER_DETAIL table
CREATE TABLE USER_DETAIL (
    User_id BIGINT PRIMARY KEY REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Star_sign VARCHAR(20) CHECK (Star_sign IN ('摩羯', '水瓶', '雙魚', '牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手')),
    Mbti VARCHAR(5) CHECK (Mbti IN ('ISTP', 'ISFP', 'ESTP', 'ESFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'INTP', 'INTJ', 'ENTP', 'ENTJ', 'INFJ', 'INFP', 'ENFJ', 'ENFP')),
    Blood_type VARCHAR(5) CHECK (Blood_type IN ('A', 'B', 'AB', 'O')),
    Religion VARCHAR(15) CHECK (Religion IN ('無', '佛教', '道教', '基督教', '天主教', '伊斯蘭教', '印度教', '其他')),
    University VARCHAR(50),
    Married VARCHAR(5) CHECK (Married IN ('未婚', '已婚', '喪偶')),
    Sns VARCHAR(5) CHECK (Sns IN ('YES', 'NO')),
    Self_introduction VARCHAR(200),
    Interest VARCHAR(200),
    Find_meeting_type VARCHAR(50)
);

-- Create USER_ROLE table
CREATE TABLE USER_ROLE (
    User_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Role VARCHAR(10) CHECK (Role IN ('User', 'Admin')),
    PRIMARY KEY (User_id, Role)
);

-- Create MEETING table
CREATE TABLE MEETING (
    Meeting_id BIGINT PRIMARY KEY,
    Holder_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Content VARCHAR(50) NOT NULL CHECK (Content IN ('午餐', '咖啡/下午茶', '晚餐', '喝酒', '語言交換')),
    Event_date DATE NOT NULL,
    Start_time TIME NOT NULL,
    End_time TIME NOT NULL,
    Event_city VARCHAR(20) NOT NULL,
    Event_place VARCHAR(50) NOT NULL,
    Status VARCHAR(20) NOT NULL CHECK (Status IN ('Ongoing', 'Finished', 'Canceled')),
    Num_participant INTEGER NOT NULL,
    Max_num_participant INTEGER
);

-- Create MEETING_LANGUAGE table
CREATE TABLE MEETING_LANGUAGE (
    Meeting_id BIGINT REFERENCES MEETING(Meeting_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Language VARCHAR(40) CHECK (Language IN ('中文', '台語', '客語', '原住民語', '英文', '日文', '韓文', '法文', '德文', '西班牙文', '俄文', '阿拉伯文', '泰文', '越南文', '印尼文')),
    PRIMARY KEY (Meeting_id, Language)
);

-- Create PARTICIPATION table
CREATE TABLE PARTICIPATION (
    User_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Meeting_id BIGINT REFERENCES MEETING(Meeting_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Join_time TIMESTAMP NOT NULL,
    PRIMARY KEY (User_id, Meeting_id)
);

-- Create SNS_DETAIL table
CREATE TABLE SNS_DETAIL (
    User_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Sns_type VARCHAR(10) CHECK (Sns_type IN ('Facebook', 'Instagram', 'Threads', 'X', 'Tiktok', '小紅書', 'WhatsApp', 'LINE', 'WeChat', 'KakaoTalk')),
    Sns_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (User_id, Sns_type)
);

-- Create CHATTING_ROOM table
CREATE TABLE CHATTING_ROOM (
    Meeting_id BIGINT REFERENCES MEETING(Meeting_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Sender_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Sending_time TIMESTAMP,
    Content VARCHAR(200),
    PRIMARY KEY (Meeting_id, Sender_id, Sending_time)
);

-- Create PRIVATE_MESSAGE table
CREATE TABLE PRIVATE_MESSAGE (
    Sender_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Receiver_id BIGINT REFERENCES "USER"(User_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Sending_time TIMESTAMP,
    Content VARCHAR(200),
    PRIMARY KEY (Sender_id, Receiver_id, Sending_time)
);