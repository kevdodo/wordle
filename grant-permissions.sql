DROP USER IF EXISTS 'wordleclient'@'localhost';
DROP USER IF EXISTS 'wordleadmin'@'localhost';

-- Create a user named wordleclient that can access the shop and the stats
-- tables and execute the stored procedures and functions.
CREATE USER 'wordleclient'@'localhost';
GRANT USAGE ON *.* TO `wordleclient`@`localhost`;
GRANT SELECT ON `wordledb`.`shop` TO `wordleclient`@`localhost`;
GRANT SELECT ON `wordledb`.`player_stats` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_add_guess` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_create_player` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`fetch_player_items` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_use_buy_item` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_game_won` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`get_player_info` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_change_password` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON PROCEDURE `wordledb`.`sp_get_player_stats` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON FUNCTION `wordledb`.`sp_new_game` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON FUNCTION `wordledb`.`authenticate` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON FUNCTION `wordledb`.`get_random_fact` TO `wordleclient`@`localhost`;
GRANT EXECUTE ON FUNCTION `wordledb`.`get_random_word` TO `wordleclient`@`localhost`;

-- Create a user named wordleadmin with the password 'ilovewordle'
CREATE USER 'wordleadmin'@'localhost' IDENTIFIED BY 'ilovewordle';
GRANT USAGE ON *.* TO `wordleadmin`@`localhost`;
GRANT ALL PRIVILEGES ON `wordledb`.* TO `wordleadmin`@`localhost` WITH GRANT OPTION;