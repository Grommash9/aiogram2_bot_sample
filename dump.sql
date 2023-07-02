DROP TABLE IF EXISTS `data_tg_user`;

CREATE TABLE `data_tg_user`
(
    `user_id`   bigint     NOT NULL,
    `name`      varchar(200) DEFAULT NULL,
    `user_name` varchar(100) DEFAULT NULL,
    `balance`   float        DEFAULT NULL,
    `language`  varchar(4) NOT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

