-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: PDS
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `total_pizzas_ordered` int DEFAULT NULL,
  `gender` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Big Bossman','1990-01-01','123456789','1234AB','admin','$2b$12$h6yDXa5eTFGgApMDck6sWOR06OfQUVfLa/wtTkRDlOWEF/E4bx89S',0,'male'),(2,'Testy Tester','2005-02-01','987654321','6211NE','test123','$2b$12$i3iz7XwfUm9OKmlQ2rdCpuJcEPi0aE4GimzpNbTcLszs5Fo8BHWAK',14,'female'),(3,'Pizza Lover','2005-10-12','129834765','6219KE','pizzalover123','$2b$12$Zb7v9HyfEynI0/Uu3epjJOHdTkSB2lP35Bk6l7ctQyq3kTJyMemBW',0,'female'),(4,'Anthony Edwards','2019-02-20','234523746','6219KE','nba12','$2b$12$.JY0Rr3TroT6J861GKSSVu8W0U8rsH5xZmLPpGs8h.JB0bsQ0DpAi',4,'male'),(5,'Lebron James','2019-09-18','2342342','6211NE','nba134','$2b$12$6MALm.BnWLSn/5ov.MVTHunsu4N1b48PbaHweKkMx3o5LE38R1Ex2',6,'male'),(6,'Test Testy','2001-05-14','987654321','6215KE','test321','$2b$12$szO/mlZX28/EkFLDRnb9nuCOKhjmYHFeXPVUSuUogLzOrjftJo3OK',6,'other');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery`
--

DROP TABLE IF EXISTS `delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery` (
  `delivery_id` int NOT NULL AUTO_INCREMENT,
  `deliverer_id` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`delivery_id`),
  KEY `deliverer_id` (`deliverer_id`),
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`deliverer_id`) REFERENCES `delivery_person` (`deliverer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery`
--

LOCK TABLES `delivery` WRITE;
/*!40000 ALTER TABLE `delivery` DISABLE KEYS */;
INSERT INTO `delivery` VALUES (1,9,'2024-10-12 23:02:38','Delivered'),(2,1,'2024-10-12 23:03:08','Delivered'),(4,1,'2024-10-12 23:25:41','Delivered'),(6,1,'2024-10-12 23:40:36','Delivered'),(7,9,'2024-10-12 23:42:01','Delivered'),(9,9,'2024-10-12 23:42:31','Delivered'),(10,1,'2024-10-12 23:53:29','Delivered'),(11,1,'2024-10-12 23:54:17','Delivered'),(14,1,'2024-10-13 00:02:17','Delivered'),(21,5,'2024-10-14 22:08:44','Delivered'),(22,5,'2024-10-14 22:08:57','Delivered');
/*!40000 ALTER TABLE `delivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_order`
--

DROP TABLE IF EXISTS `delivery_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_order` (
  `delivery_id` int NOT NULL,
  `order_id` int NOT NULL,
  PRIMARY KEY (`delivery_id`,`order_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `delivery_order_ibfk_1` FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`delivery_id`),
  CONSTRAINT `delivery_order_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_order`
--

LOCK TABLES `delivery_order` WRITE;
/*!40000 ALTER TABLE `delivery_order` DISABLE KEYS */;
INSERT INTO `delivery_order` VALUES (1,5),(2,6),(4,8),(4,9),(6,12),(7,13),(9,15),(10,17),(10,18),(11,19),(14,22),(21,32),(22,33),(21,34);
/*!40000 ALTER TABLE `delivery_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_person`
--

DROP TABLE IF EXISTS `delivery_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_person` (
  `deliverer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  `postal_code` varchar(4) DEFAULT NULL,
  `next_available` datetime DEFAULT NULL,
  PRIMARY KEY (`deliverer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_person`
--

LOCK TABLES `delivery_person` WRITE;
/*!40000 ALTER TABLE `delivery_person` DISABLE KEYS */;
INSERT INTO `delivery_person` VALUES (1,'Deliverer 1',1,'6211','2024-10-13 00:05:47'),(2,'Deliverer 2',1,'6212',NULL),(3,'Deliverer 3',1,'6213',NULL),(4,'Deliverer 4',1,'6214',NULL),(5,'Deliverer 5',1,'6215','2024-10-14 22:15:14'),(6,'Deliverer 6',1,'6216',NULL),(7,'Deliverer 7',1,'6217',NULL),(8,'Deliverer 8',1,'6218',NULL),(9,'Deliverer 9',1,'6219','2024-10-12 23:48:31');
/*!40000 ALTER TABLE `delivery_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dessert`
--

DROP TABLE IF EXISTS `dessert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dessert` (
  `dessert_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `cost` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`dessert_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dessert`
--

LOCK TABLES `dessert` WRITE;
/*!40000 ALTER TABLE `dessert` DISABLE KEYS */;
INSERT INTO `dessert` VALUES (1,'Flavor Explosion',8.00),(2,'Pompeii Lava Cake',7.90);
/*!40000 ALTER TABLE `dessert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discount_code`
--

DROP TABLE IF EXISTS `discount_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount_code` (
  `code` varchar(7) NOT NULL,
  `discount_percent` decimal(3,2) DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount_code`
--

LOCK TABLES `discount_code` WRITE;
/*!40000 ALTER TABLE `discount_code` DISABLE KEYS */;
INSERT INTO `discount_code` VALUES ('ASDFG2',0.15,'2024-11-11'),('HJKLZ5',0.13,'2024-11-11'),('JNHBG8',0.08,'2024-11-11'),('MNBVC6',0.19,'2024-11-11'),('PLMKO7',0.22,'2024-11-11'),('QAZWS9',0.25,'2024-11-11'),('QWERT1',0.10,'2024-11-11'),('XEDCR0',0.17,'2024-11-11'),('YUIOP4',0.05,'2024-11-11'),('ZXCVB3',0.20,'2024-11-11');
/*!40000 ALTER TABLE `discount_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drink`
--

DROP TABLE IF EXISTS `drink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drink` (
  `drink_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `cost` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`drink_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drink`
--

LOCK TABLES `drink` WRITE;
/*!40000 ALTER TABLE `drink` DISABLE KEYS */;
INSERT INTO `drink` VALUES (1,'Cloudy White Milkshake',3.50),(2,'Get Drunk(10 Shot Cocktail)',9.50);
/*!40000 ALTER TABLE `drink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `cost` decimal(5,2) DEFAULT NULL,
  `is_vegetarian` tinyint(1) DEFAULT NULL,
  `is_vegan` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Mozzarella Cheese',1.50,1,0),(2,'Vegan Mozzarella Cheese',2.00,1,1),(3,'Cheddar Cheese',1.50,1,0),(4,'Parmesan Cheese',1.75,1,0),(5,'Gorgonzola Cheese',2.00,1,0),(6,'Tomato Sauce',0.50,1,1),(7,'Pizza Dough',2.00,1,1),(8,'Pepperoni',3.00,0,0),(9,'Pineapple',1.00,1,1),(10,'Bell Pepper',0.75,1,1),(11,'Onion',0.50,1,1),(12,'Black Olives',1.00,1,1),(13,'Chicken',3.50,0,0),(14,'Curry Sauce',1.50,1,1),(15,'Kebab Meat',3.50,0,0),(16,'Gyros Meat',3.00,0,0),(17,'Jalape├▒os',0.75,1,1),(18,'Black Beans',0.75,1,1),(19,'Italian Sausage',3.00,0,0);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_dessert`
--

DROP TABLE IF EXISTS `order_dessert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_dessert` (
  `dessert_id` int NOT NULL,
  `order_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`dessert_id`,`order_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_dessert_ibfk_1` FOREIGN KEY (`dessert_id`) REFERENCES `dessert` (`dessert_id`),
  CONSTRAINT `order_dessert_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_dessert`
--

LOCK TABLES `order_dessert` WRITE;
/*!40000 ALTER TABLE `order_dessert` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_dessert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_drink`
--

DROP TABLE IF EXISTS `order_drink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_drink` (
  `drink_id` int NOT NULL,
  `order_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`drink_id`,`order_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_drink_ibfk_1` FOREIGN KEY (`drink_id`) REFERENCES `drink` (`drink_id`),
  CONSTRAINT `order_drink_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_drink`
--

LOCK TABLES `order_drink` WRITE;
/*!40000 ALTER TABLE `order_drink` DISABLE KEYS */;
INSERT INTO `order_drink` VALUES (2,12,1);
/*!40000 ALTER TABLE `order_drink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_pizza`
--

DROP TABLE IF EXISTS `order_pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_pizza` (
  `pizza_id` int NOT NULL,
  `order_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`pizza_id`,`order_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_pizza_ibfk_1` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`pizza_id`),
  CONSTRAINT `order_pizza_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_pizza`
--

LOCK TABLES `order_pizza` WRITE;
/*!40000 ALTER TABLE `order_pizza` DISABLE KEYS */;
INSERT INTO `order_pizza` VALUES (1,12,1),(1,15,1),(1,17,1),(1,32,1),(1,33,1),(2,5,2),(2,8,1),(2,13,1),(2,18,1),(2,19,1),(2,22,1),(2,32,1),(2,33,1),(3,9,1),(3,13,1),(3,18,1),(3,19,1),(3,33,1),(4,34,1),(5,6,1),(5,9,1);
/*!40000 ALTER TABLE `order_pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `order_datetime` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `eta` datetime DEFAULT NULL,
  `delivery_address` varchar(50) DEFAULT NULL,
  `total_price` decimal(7,2) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (5,2,'2024-10-12 23:02:08','Delivered','2024-10-12 23:04:08','6219KE',30.52),(6,2,'2024-10-12 23:02:38','Delivered','2024-10-12 23:04:38','6211NE',6.18),(8,2,'2024-10-12 23:25:10','Delivered','2024-10-12 23:27:11','6211NE',13.73),(9,2,'2024-10-12 23:25:29','Delivered','2024-10-12 23:27:29','6211NE',13.05),(12,4,'2024-10-12 23:40:06','Delivered','2024-10-12 23:42:06','6211NE',23.62),(13,4,'2024-10-12 23:41:31','Delivered','2024-10-12 23:43:31','6219KE',22.89),(15,4,'2024-10-12 23:42:01','Delivered','2024-10-12 23:44:01','6219KE',14.12),(17,5,'2024-10-12 23:52:58','Delivered','2024-10-12 23:51:06','6211NE',14.12),(18,5,'2024-10-12 23:53:17','Delivered','2024-10-12 23:51:06','6211NE',22.89),(19,5,'2024-10-12 23:53:47','Delivered','2024-10-12 23:55:47','6211NE',22.89),(22,5,'2024-10-13 00:01:46','Delivered','2024-10-13 00:03:47','6211NE',13.73),(32,6,'2024-10-14 22:08:14','Delivered','2024-10-14 22:10:44','6215KE',29.38),(33,6,'2024-10-14 22:08:26','Delivered','2024-10-14 22:13:27','6215KE',37.01),(34,6,'2024-10-14 22:08:37','Delivered','2024-10-14 22:11:07','6215KE',9.54);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza` (
  `pizza_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pizza_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (1,'Gooey Cheese ALL Over Your Face (Four Cheese Pizza)'),(2,'So Not Halal Mode (Pepperoni Pizza)'),(3,'Performance Enhancer (Pineapple Pizza)'),(4,'Veggie Virgin (Vegetarian Pizza)'),(5,'Vegan (Cheese Pizza)'),(6,'Indian Classic (Chicken Curry Pizza)'),(7,'Mexico\'s Finest(Mexican Pizza)'),(8,'O\'Block (Chicago\'s Finest Pizza)'),(9,'Arab All the Way! (Kebab Pizza)'),(10,'The Greek Freak (Gyros Pizza)');
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza_ingredient`
--

DROP TABLE IF EXISTS `pizza_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza_ingredient` (
  `pizza_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  PRIMARY KEY (`pizza_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `pizza_ingredient_ibfk_1` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`pizza_id`),
  CONSTRAINT `pizza_ingredient_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza_ingredient`
--

LOCK TABLES `pizza_ingredient` WRITE;
/*!40000 ALTER TABLE `pizza_ingredient` DISABLE KEYS */;
INSERT INTO `pizza_ingredient` VALUES (1,1),(2,1),(3,1),(4,1),(6,1),(7,1),(8,1),(9,1),(10,1),(5,2),(1,3),(8,3),(1,4),(1,5),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(2,8),(8,8),(3,9),(4,10),(4,11),(4,12),(6,13),(6,14),(9,15),(10,16),(7,17),(7,18),(2,19),(8,19);
/*!40000 ALTER TABLE `pizza_ingredient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-15 15:39:13
