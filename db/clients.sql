CREATE TABLE `clients_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `gender` enum('M','F','I') NOT NULL,
  `phone` varchar(14) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf` (`cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;

INSERT INTO `clients_data` VALUES (1,'Mauricio Cordeiro','06673469021','mauricio@hotmail.com','M','(11)98725-6530'),(2,'Maria Ribeiro','11262672015','maria.ribeiro@hotmail.com','F','(58)92607-6630'),(3,'Julia Oliveira','26733962098','julia.oliveira@gmail.com','F','(57)92017-9365'),(4,'Billy Jimmy','55486213549','billy@uol.com','M','(16)955644825'),(7,'Fernando Ramos','54621358789','ramos@hotmail.com','M','(18)956213457'),(8,'Lucas Sauro','54621358528','sauro_lucas@hotmail.com','M','(11)985213457'),(23,'Julia Roberts','89762146259','Julia@gmail.com','F','(11)958468458'),(25,'Lucas Bento','8854624658','lucas@teste.com','M','(11)954524658'),(57,'Lucas Sauro','54621357528','sauro_lucas@hotmail.com','M','(11)985213457');

CREATE TABLE `address` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `number` int(4) NOT NULL,
  `street` varchar(50) NOT NULL,
  `complement` varchar(50) DEFAULT NULL,
  `neighborhod` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `country` varchar(50) DEFAULT 'Brasil',
  `zipcode` varchar(9) NOT NULL,
  `clientid` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clientid` (`clientid`),
  CONSTRAINT `address_ibfk_1` FOREIGN KEY (`clientid`) REFERENCES `clients_data` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

INSERT INTO `address` VALUES (1,101,'Rua Pato','Apartamento 101','Copacabana','Rio de Janeiro','Rio de Janeiro','Brasil','12345-678',1),(2,342,'Rua Bird','Condiminio Flores','Lourdes','Belo Horizonte','Minas Gerais','Brasil','48314-789',1),(3,863,'Rua Cachorro','Casa','Pinheiros','São Paulo','São Paulo','Brasil','95647-356',2),(4,1930,'Rua Porco','Casa B','Vila Yara','São Paulo','São Paulo','Brasil','78963-612',3),(5,101,'Rua Billy','','Catarin','Florianopolis','Santa Catarina','Brasil','12345-789',25),(6,55,'Rua sea','','Jeric','Jericoacoara','Jericoacoara','Brasil','123123-78',23),(7,88,'Rua earth','','Espirit','Vitoria','Espirito Santo','Brasil','123123-22',7),(13,88,'Rua earth','','Espirit','Vitoria','Espirito Santo','Brasil','123123-22',4),(16,88,'Rua earth','','Espirit','Vitoria','Espirito Santo','Brasil','123123-22',7),(17,88,'Rua earth','','Espirit','asdfhhasdjkf','Espirito Santo','Brasil','123123-22',7);
