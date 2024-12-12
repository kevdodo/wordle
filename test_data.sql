-- TODO: create fake profiles and stuff

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('bruh', SHA2('lol', 256), 'hi', 'desc')

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player2', SHA2('lol', 256), 'hi', 'desc')

INSERT INTO player_info (username, password_hash, salt, email) VALUES ('player2', SHA2('lol', 256), 'hi', 'desc')

INSERT INTO player_items (player_id, item_id, quantity) VALUES (1, 1, 1);

INSERT INTO games_played (player_id, word_id, finish_time_sec, num_guesses ) VALUES (1, 2, 3, 4)

INSERT INTO guesses (game_id, guess, guess_number) VALUES (1, 'apple', 1) 

INSERT INTO guesses (game_id, guess, guess_number) VALUES (2, 'apple', 1) 

INSERT INTO guesses (game_id, guess, guess_number) VALUES (3, 'apple', 1) 