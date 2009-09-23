CREATE DATABASE IF NOT EXISTS `pysawndz`;

USE `pysawndz`;

DROP TABLE IF EXISTS `albums`;

CREATE TABLE `albums` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `artist_id` INT(11) NOT NULL,
  `name` TEXT,
  `album_date` DATE NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `artists`;

CREATE TABLE `artists` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `genres`;

CREATE TABLE `genres` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `playlist_songs`;

CREATE TABLE `playlist_songs` (
  `playlist_id` INT(11) NOT NULL,
  `song_id` INT(11) NOT NULL
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `playlists`;

CREATE TABLE `playlists` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `songs`;

CREATE TABLE `songs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `artist_id` INT(11) NOT NULL,
  `album_id` INT(11) NOT NULL,
  `genre_id` INT(11) NOT NULL,
  `title` TEXT,
  `duration` INT(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

