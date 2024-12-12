-- Delete functions and procedures if they exist
DROP FUNCTION IF EXISTS authenticate;
DROP FUNCTION IF EXISTS make_salt;
DROP PROCEDURE IF EXISTS sp_create_player;
DROP PROCEDURE IF EXISTS sp_change_password;


-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Authenticates the specified username and password against the data
-- in the player_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN

  DECLARE user_found TINYINT DEFAULT (
    SELECT COUNT(*)
    FROM player_info as u
    WHERE u.username = username
    AND u.password_hash = SHA2(CONCAT(u.salt, password), 256)
    );

  RETURN user_found;

END !
DELIMITER ;


DELIMITER !
CREATE PROCEDURE sp_create_player(new_username VARCHAR(20), 
                                    password VARCHAR(20),
                                    email VARCHAR(50),
                                    player_description VARCHAR(500))
BEGIN

  DECLARE new_salt CHAR(8);
  DECLARE password_hash BINARY(64);
  DECLARE new_hash BINARY(64);

  SET new_salt = make_salt(8);

  SET new_hash = SHA2(CONCAT(new_salt, password), 256);

  IF new_username = '' OR password = ''
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username and password cannot be empty';
  END IF;
  IF LENGTH(new_username) > 20 OR LENGTH(password) > 20
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username and password cannot be longer than 20 characters';
  END IF;
  IF (SELECT COUNT(*) from player_info WHERE username = new_username) > 0
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User already exists';
  END IF;

  INSERT INTO player_info (username, password_hash, salt, email, player_description) VALUES (new_username, new_hash, new_salt, email, player_description);
END !
DELIMITER ;


-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(username VARCHAR(100), new_password VARCHAR(100))
BEGIN

  DECLARE new_salt CHAR(8) DEFAULT make_salt(8);
  DECLARE new_hash VARCHAR(28) DEFAULT '';

  IF username = '' OR new_password = ''
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username and password cannot be empty';
  END IF;
  IF LENGTH(username) > 20 OR LENGTH(new_password) > 20
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username and password cannot be longer than 20 characters';
  END IF;
  IF (SELECT COUNT(*) from player_info WHERE username = username) = 0
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User does not exist';
  END IF;

  SET new_hash = SHA2(CONCAT(new_salt, new_password), 256);

  UPDATE player_info as u
  SET u.salt = new_salt, u.password_hash = new_hash
  WHERE u.username = username;

END !
DELIMITER ;