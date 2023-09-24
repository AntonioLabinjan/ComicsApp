CREATE DATABASE ComicsApp;
USE ComicsApp;
CREATE TABLE Comic (
	comic_identificator INT PRIMARY KEY,
	comic_name VARCHAR(100),
	comic_number INT,
	comic_hero VARCHAR(100),
	comic_pageNum INT,
	comic_publisher VARCHAR(100)
	);
