-- Delete functions and procedures if they exist
DROP FUNCTION IF EXISTS compute_score;
DROP PROCEDURE IF EXISTS hardest_words;
DROP PROCEDURE IF EXISTS unplayed_words;
DROP PROCEDURE IF EXISTS get_player_items;
DROP FUNCTION IF EXISTS unplayed_words;
DROP PROCEDURE IF EXISTS sp_use_buy_item;
DROP PROCEDURE IF EXISTS fetch_player_items;
DROP PROCEDURE IF EXISTS sp_update_stats;
DROP PROCEDURE IF EXISTS sp_get_player_stats;
DROP TRIGGER IF EXISTS trg_update_stats;

DROP FUNCTION IF EXISTS get_random_word;
DROP FUNCTION IF EXISTS get_random_fact;
DROP FUNCTION IF EXISTS sp_new_game;
DROP PROCEDURE IF EXISTS sp_add_guess;
DROP PROCEDURE IF EXISTS get_player_info;
DROP PROCEDURE IF EXISTS sp_game_won;


-- Create a function that computes a players score based off 
-- of the number of guesses and the time it took to finish the game.
DELIMITER !
CREATE FUNCTION compute_score(finish_time_sec INT, num_guesses INT) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE score INT;
    SET score = 1000 - (num_guesses * 10) - (finish_time_sec / 10);

    -- if they took too long
    IF score < 0 THEN
        SET score = 0;
    END IF;
    RETURN score;
END !
DELIMITER ;


-- List the hardest words by getting the average finish time and number of guesses for each word.
DELIMITER !
CREATE PROCEDURE hardest_words()
BEGIN
    SELECT word, AVG(finish_time_sec) AS avg_finish_time, AVG(num_guesses) AS avg_num_guesses
    FROM games_played NATURAL JOIN words
    GROUP BY word
    ORDER BY avg_num_guesses DESC, avg_finish_time DESC;
END !
DELIMITER ;


-- Get words that have never been played or solved by any player
DELIMITER !
CREATE FUNCTION unplayed_words()
BEGIN
    SELECT word FROM words WHERE word_id NOT IN (SELECT word_id FROM games_played);
END !
DELIMITER ;


DELIMITER !
CREATE PROCEDURE sp_use_buy_item(player_id_temp INT, item_id_temp INT, num_items_temp INT)
BEGIN
    DECLARE total_items INT;
    DECLARE item_cost INT DEFAULT (SELECT item_cost FROM shop WHERE item_id = item_id_temp);
    -- Update the number of items bought
    IF NOT (SELECT 1 FROM player_items WHERE (player_id = player_id_temp) AND  (item_id = item_id_temp)) THEN
        IF num_items_temp > 0 THEN
            INSERT INTO player_items (player_id, item_id, quantity) VALUES (player_id_temp, item_id_temp, num_items_temp);
            END IF;
        -- Should not be able to use an item it doesn't have
    ELSE
        SET total_items = (SELECT quantity + num_items_temp FROM player_items WHERE (player_id = player_id_temp) AND (item_id = item_id_temp));

        IF (total_items = 0) THEN      
            DELETE FROM player_items WHERE player_id = player_id_temp AND item_id = player_id_temp;
        END IF;
    END IF;
    IF (num_items_temp > 0) THEN
        UPDATE player_info SET num_coins = num_coins - item_cost*num_items_temp WHERE player_id = player_id_temp;
    END IF; 
END !
DELIMITER ;


-- Fetch Player Items
DELIMITER !
CREATE PROCEDURE fetch_player_items(player_id INT)
BEGIN
    SELECT item_id, item_name, quantity, item_cost FROM player_items AS i NATURAL JOIN shop WHERE i.player_id = player_id;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION get_random_word() RETURNS VARCHAR(50) DETERMINISTIC
BEGIN
    DECLARE random_word VARCHAR(50);
    SELECT word INTO random_word FROM words WHERE possible = 1
    ORDER BY RAND()
    LIMIT 1;
    RETURN random_word;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION get_random_fact() RETURNS VARCHAR(50) DETERMINISTIC
BEGIN
    DECLARE random_fact VARCHAR(50);
    SELECT fact INTO random_fact FROM fun_facts
    ORDER BY RAND()
    LIMIT 1;
    RETURN random_fact;
    RETURN random_fact;
END !
DELIMITER ;



DELIMITER !
CREATE PROCEDURE sp_new_game(player_id_temp INT, word_id_temp INT)
BEGIN
    INSERT INTO games_played (player_id, word_id) VALUES (player_id_temp, word_id_temp);
    SELECT game_id FROM games_played WHERE (player_id = player_id) AND (word_id = word_id_temp);
END !

DELIMITER ;

DELIMITER !

CREATE PROCEDURE sp_add_guess(game_id INT, guess VARCHAR(10), attempts INT)
BEGIN
    INSERT INTO guesses (game_id, guess, guess_number) VALUES (game_id, guess, attempts);
END !


DELIMITER !

CREATE PROCEDURE sp_update_stats(game_id_temp INT)
BEGIN
    UPDATE player_stats SET 
        avg_score = (SELECT AVG(score) as avg_score FROM games_played WHERE player_id = (SELECT player_id FROM games_played WHERE game_id = game_id_temp)), 

        avg_guesses = (SELECT AVG(num_guesses) as avg_guesses FROM games_played WHERE player_id = (SELECT player_id FROM games_played WHERE game_id = game_id_temp)),

        avg_solve_time = (SELECT AVG(finish_time_sec) as avg_solve_time FROM games_played WHERE player_id = (SELECT player_id FROM games_played WHERE game_id = game_id_temp)),

        avg_guess_time = (SELECT AVG(guess_time) avg_guess_time FROM games_played WHERE player_id = (SELECT player_id FROM games_played WHERE game_id = game_id_temp));
END !

create

DELIMITER ;

DELIMITER !

CREATE PROCEDURE get_player_info (username VARCHAR(50))
BEGIN
    SELECT * FROM player_info as p where p.username = username;
END !
DELIMITER ;


DELIMITER !

CREATE TRIGGER trg_update_stats AFTER UPDATE ON games_played
FOR EACH ROW
BEGIN
    CALL sp_update_stats(NEW.player_id, NEW.finish_time_sec, NEW.num_guesses);
END !

DELIMITER ;

DELIMITER !

CREATE PROCEDURE sp_game_won(player_id_temp INT, finish_time_temp INT, num_guesses_temp INT)
BEGIN
    DECLARE SCORE INT;
    SELECT compute_score(finish_time_temp, num_guesses_temp) INTO SCORE;
    UPDATE player_info SET num_coins = num_coins + SCORE WHERE player_id = player_id_temp;
END !

DELIMITER ;
