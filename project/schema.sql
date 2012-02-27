-- MySQL dump 10.13  Distrib 5.1.58, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: epf
-- ------------------------------------------------------
-- Server version	5.1.58-1ubuntu1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `epf_application`
--

DROP TABLE IF EXISTS `epf_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_application` (
  `export_date` bigint(20) DEFAULT NULL,
  `application_id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(1000) DEFAULT NULL,
  `recommended_age` varchar(20) DEFAULT NULL,
  `artist_name` varchar(1000) DEFAULT NULL,
  `seller_name` varchar(1000) DEFAULT NULL,
  `company_url` varchar(1000) DEFAULT NULL,
  `support_url` varchar(1000) DEFAULT NULL,
  `view_url` varchar(1000) DEFAULT NULL,
  `artwork_url_large` varchar(1000) DEFAULT NULL,
  `artwork_url_small` varchar(1000) DEFAULT NULL,
  `itunes_release_date` datetime DEFAULT NULL,
  `copyright` varchar(4000) DEFAULT NULL,
  `description` longtext,
  `version` varchar(100) DEFAULT NULL,
  `itunes_version` varchar(100) DEFAULT NULL,
  `download_size` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`application_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_application_detail`
--

DROP TABLE IF EXISTS `epf_application_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_application_detail` (
  `export_date` bigint(20) DEFAULT NULL,
  `application_id` int(11) NOT NULL DEFAULT '0',
  `language_code` varchar(20) NOT NULL DEFAULT '',
  `title` varchar(1000) DEFAULT NULL,
  `description` longtext,
  `release_notes` longtext,
  `company_url` varchar(1000) DEFAULT NULL,
  `support_url` varchar(1000) DEFAULT NULL,
  `screenshot_url_1` varchar(1000) DEFAULT NULL,
  `screenshot_url_2` varchar(1000) DEFAULT NULL,
  `screenshot_url_3` varchar(1000) DEFAULT NULL,
  `screenshot_url_4` varchar(1000) DEFAULT NULL,
  `screenshot_width_height_1` varchar(20) DEFAULT NULL,
  `screenshot_width_height_2` varchar(20) DEFAULT NULL,
  `screenshot_width_height_3` varchar(20) DEFAULT NULL,
  `screenshot_width_height_4` varchar(20) DEFAULT NULL,
  `ipad_screenshot_url_1` varchar(1000) DEFAULT NULL,
  `ipad_screenshot_url_2` varchar(1000) DEFAULT NULL,
  `ipad_screenshot_url_3` varchar(1000) DEFAULT NULL,
  `ipad_screenshot_url_4` varchar(1000) DEFAULT NULL,
  `ipad_screenshot_width_height_1` varchar(20) DEFAULT NULL,
  `ipad_screenshot_width_height_2` varchar(20) DEFAULT NULL,
  `ipad_screenshot_width_height_3` varchar(20) DEFAULT NULL,
  `ipad_screenshot_width_height_4` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`application_id`,`language_code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_application_device_type`
--

DROP TABLE IF EXISTS `epf_application_device_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_application_device_type` (
  `export_date` bigint(20) DEFAULT NULL,
  `application_id` int(11) NOT NULL DEFAULT '0',
  `device_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`application_id`,`device_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_application_price`
--

DROP TABLE IF EXISTS `epf_application_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_application_price` (
  `export_date` bigint(20) DEFAULT NULL,
  `application_id` int(11) NOT NULL DEFAULT '0',
  `retail_price` decimal(9,3) DEFAULT NULL,
  `currency_code` varchar(20) DEFAULT NULL,
  `storefront_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`application_id`,`storefront_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_device_type`
--

DROP TABLE IF EXISTS `epf_device_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_device_type` (
  `export_date` bigint(20) DEFAULT NULL,
  `device_type_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`device_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_genre`
--

DROP TABLE IF EXISTS `epf_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_genre` (
  `export_date` bigint(20) DEFAULT NULL,
  `genre_id` int(11) NOT NULL DEFAULT '0',
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`genre_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `epf_genre_application`
--

DROP TABLE IF EXISTS `epf_genre_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `epf_genre_application` (
  `export_date` bigint(20) DEFAULT NULL,
  `genre_id` int(11) NOT NULL DEFAULT '0',
  `application_id` int(11) NOT NULL DEFAULT '0',
  `is_primary` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`genre_id`,`application_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-02-27 11:43:49
