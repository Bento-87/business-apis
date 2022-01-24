CREATE TABLE `orders` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ClientId` int(11) NOT NULL,
  `ProductId` int(11) NOT NULL,
  `OrderDate` date NOT NULL,
  `Observation` mediumtext DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;

INSERT INTO `orders` VALUES (1,1,4,'2021-04-21',NULL),(2,3,1,'2021-03-12','Cartao de credito'),(3,4,1,'2021-02-09','Cheque'),(4,1,4,'2021-01-06',NULL),(5,8,6,'2021-04-19',NULL),(6,23,13,'2021-04-19',NULL),(7,57,14,'2021-04-19',NULL),(9,3,2,'2021-04-29',NULL),(11,2,2,'2021-04-29',NULL),(18,1,2,'2021-04-15',NULL),(19,1,2,'2021-04-15',NULL),(20,7,2,'2021-04-15',NULL);
