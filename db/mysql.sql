DROP TABLE IF EXISTS users;
CREATE TABLE users (
       id INT NOT NULL AUTO_INCREMENT,
       username VARCHAR(255),
       password VARCHAR(255),
       PRIMARY KEY (id)
) ENGINE = INNODB;

DROP TABLE IF EXISTS nodes;
CREATE TABLE nodes (
       id INT NOT NULL AUTO_INCREMENT,
       shortname VARCHAR(255) NOT NULL, 
       name VARCHAR(255),
       user_id INT NOT NULL,
       description TEXT,
       is_public BOOLEAN DEFAULT 0,
       access_key VARCHAR(40),
       access_password VARCHAR(40),
       PRIMARY KEY (id)
) ENGINE = INNODB;

DROP TABLE IF EXISTS addresses;
CREATE TABLE addresses (
       id INT NOT NULL AUTO_INCREMENT,
       user_id INT NOT NULL,
       value VARCHAR(255) NOT NULL, 
       verified BOOLEAN DEFAULT 0,
       mobile BOOLEAN DEFAULT 0,
       PRIMARY KEY (id)
) ENGINE = INNODB;

DROP TABLE IF EXISTS subscribers;
CREATE TABLE subscribers (
       id INT NOT NULL AUTO_INCREMENT,
       user_id INT NOT NULL,
       node_id INT NOT NULL,
       service_name VARCHAR(255) NOT NULL, 
       config TEXT,
       PRIMARY KEY (id)
) ENGINE = INNODB;

DROP TABLE IF EXISTS publishers;
CREATE TABLE publishers (
       id INT NOT NULL AUTO_INCREMENT,
       user_id INT NOT NULL,
       node_id INT NOT NULL,
       service_name VARCHAR(255) NOT NULL, 
       config TEXT,
       PRIMARY KEY (id)
) ENGINE = INNODB;

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
       id INT NOT NULL AUTO_INCREMENT,
       node_id INT NOT NULL,
       title VARCHAR(255),
       body TEXT NOT NULL, 
       PRIMARY KEY (id)
) ENGINE = INNODB;
