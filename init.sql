CREATE DATABASE IF NOT EXISTS gith;

USE gith;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS repository (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    creator_username VARCHAR(80) NOT NULL,
    FOREIGN KEY (creator_username) REFERENCES user(username),
    UNIQUE KEY unique_name_per_creator (name, creator_username)
);