
INSERT INTO shop (item_name, item_cost, item_description) VALUES ('Extra Guess', 100, 'Allows the user to make an extra guess in the game');

INSERT INTO shop (item_name, item_cost, item_description) VALUES ('Freeze Time', 100, 'Stops game time for one guess');

INSERT INTO shop (item_name, item_cost, item_description) VALUES ('Hint', 100, 'Reveals a letter in the word');

INSERT INTO shop (item_name, item_cost, item_description, one_time_purchase) VALUES ('HIDDEN 1', 500, 'Sent from the Wordle gods. I wonder what this will be....', 1);

INSERT INTO shop (item_name, item_cost, item_description) VALUES ('HIDDEN 2', 500, 'Sent from the Wordle gods. I wonder what this will be....');

LOAD DATA LOCAL INFILE 'wordle_db.csv' INTO TABLE words FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS; 

LOAD DATA LOCAL INFILE 'parsed_facts.txt' INTO TABLE fun_facts FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (fact_id, fact);



-- Create fake profiles and stuff

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('bruh', SHA2('lol', 256), 'hi', 'desc');
INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player2', SHA2('lol', 256), 'hi', 'desc');
INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player3', SHA2('lol', 256), 'hi', 'desc');
INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player4', SHA2('lol', 256), 'hi', 'desc');


INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player5', SHA2('lol', 256), 'hi', 'desc');


INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player6', SHA2('lol', 256), 'hi', 'desc');

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player7', SHA2('lol', 256), 'hi', 'desc');

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player8', SHA2('lol', 256), 'hi', 'desc');



INSERT INTO player_items (player_id, item_id, quantity) VALUES (1, 1, 1);
INSERT INTO player_items (player_id, item_id, quantity) VALUES (1, 2, 1);
INSERT INTO player_items (player_id, item_id, quantity) VALUES (1, 3, 1);
INSERT INTO player_items (player_id, item_id, quantity) VALUES (1, 4, 1);
INSERT INTO player_items (player_id, item_id, quantity) VALUES (2, 4, 1);
INSERT INTO player_items (player_id, item_id, quantity) VALUES (3, 4, 1);




INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (1, 1, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (2, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (2, 3, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (2, 4, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (2, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (3, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (3, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (1, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (2, 2, 3, 4);
INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (4, 2, 3, 4);



INSERT INTO guesses (game_id, guess, guess_number) VALUES (1, 'apple', 1);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (2, 'adieu', 1);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (3, 'apple', 1);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (3, 'reads', 2);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (4, 'adieu', 1);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (4, 'apple', 2);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (5, 'abbot', 1);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (5, 'apple', 2);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (5, 'reeks', 3);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (5, 'adieu', 4);
INSERT INTO guesses (game_id, guess, guess_number) VALUES (6, 'apple', 1); 
INSERT INTO guesses (game_id, guess, guess_number) VALUES (6, 'oiled', 2); 
INSERT INTO guesses (game_id, guess, guess_number) VALUES (6, 'peels', 3); 
INSERT INTO guesses (game_id, guess, guess_number) VALUES (6, 'nosed', 4);