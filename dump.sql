DROP TABLE IF EXISTS `data_tg_user`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_tg_user`
(
    `user_id`   bigint     NOT NULL,
    `name`      varchar(200) DEFAULT NULL,
    `user_name` varchar(100) DEFAULT NULL,
    `balance`   float        DEFAULT NULL COMMENT '' balance '',
    `language`  varchar(4) NOT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

