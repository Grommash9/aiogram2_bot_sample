CREATE TABLE IF NOT EXISTS `data_tg_user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `name` VARCHAR(255),
  `user_name` VARCHAR(255),
  `language` VARCHAR(255)
);

INSERT IGNORE INTO `data_tg_user` (`user_id`, `name`, `user_name`, `language`)
VALUES
  (12345, 'John Doe', 'johndoe', 'uk');