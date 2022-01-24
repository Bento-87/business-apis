CREATE TABLE `products` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Description` mediumtext NOT NULL,
  `Price` float(10,2) NOT NULL,
  `Availability` enum('Yes','No') NOT NULL,
  `EndOfLife` date DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

INSERT INTO `products` VALUES (1,'Fone Bluetooth','Fone de ouvido bluetooh Edifier W800-BT',70.00,'Yes',NULL),(2,'Teclado USB','Teclado USB3.0',25.00,'Yes',NULL),(3,'Mouse Gamer','Mouse Gamer 3000DPI',150.00,'Yes',NULL),(4,'Caneta 4 cores','Caneta 4 cores BIC',10.00,'No',NULL),(5,'Bloco de notas','Bloco de notas branco 1500 folhas',10.00,'No',NULL),(6,'Caderno 10 materias','Caderno 10 materias - Inmetrics',15.00,'No',NULL),(7,'Alcool em gel','Alcool em gel 1L',20.00,'Yes',NULL),(13,'Fone Bluetooth','Fone de ouvido Tronsmart Onyx Ace',150.00,'Yes',NULL),(14,'Fone Bluetooth','Fone de ouvido bluetooh Xiaomi Air Dots',80.00,'Yes','2021-06-01'),(17,'Fone Bluetooth','Fone de ouvido JBL T500',205.00,'No',NULL);