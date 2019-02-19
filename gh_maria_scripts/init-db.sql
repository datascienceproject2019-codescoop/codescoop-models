CREATE DATABASE `github`;
CREATE USER 'github-user'@'localhost' IDENTIFIED BY 'github-pass';
GRANT ALL PRIVILEGES ON `github`.* TO 'github-user'@'localhost' IDENTIFIED BY 'github-pass';