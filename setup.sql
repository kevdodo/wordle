
/*
Database Design Language Statements for the Final Project which is a SQL + Python implementation of Wordle. We are storing user info, hashing passwords, creating a shop where users can buy goodies and items to help them in the game, and storing game data such as the words, guesses, and scores.
*/
DROP DATABASE IF EXISTS wordledb;
CREATE DATABASE wordledb;
USE wordledb;



/*
Stores information about players in a game. Each player is identified by a unique player_id and has a username, password hash, email, creation timestamp, description, and number of coins.

Columns:
- player_id: SERIAL PRIMARY KEY - Unique identifier for each player.
- username: VARCHAR(50) NOT NULL - The username of the player.
- password_hash: BINARY(64) NOT NULL - The hashed password of the player in hexademical.
- email: VARCHAR(50) NOT NULL - The email address of the player.
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP - The timestamp when the player was created.
- description: VARCHAR(500) - A description or bio of the player.
- num_coins: INT NOT NULL - The number of coins the player has.
*/
CREATE TABLE player_info (
    player_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash BINARY(64) NOT NULL,
    salt CHAR(8) NOT NULL DEFAULT "",
    email VARCHAR(50) NOT NULL,
    player_description VARCHAR(200) DEFAULT "Nothing yet :()",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    num_coins INT NOT NULL DEFAULT 100
);


/*
 Stores a collection of words.
 Each row represents a single word and its associated information.
 
 Columns:
 - id: The unique identifier for the word.
 - word: The actual word.
 - length: The length of the word.
 - frequency: The frequency of the word in a given context.
 - created_at: The timestamp when the word was created.
 - updated_at: The timestamp when the word was last updated.
*/
CREATE TABLE words (
    word_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(10) UNIQUE NOT NULL,
    word_length INT NOT NULL,
    -- uncommon words should not be possible answers
    possible_answer boolean NOT NULL
);


/*
 Stores information about the games played by users.

 Columns:
   - game_id: The unique identifier for each game.
   - user_id: The unique identifier for each user.
   - game_date: The date when the game was played.
   - score: The score achieved by the user in the game.
*/
CREATE TABLE games_played (
    game_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    player_id INT UNSIGNED,
    word_id INT UNSIGNED,
    finish_time_sec INT UNSIGNED DEFAULT NULL,
    num_guesses INT DEFAULT 5,
    score INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES player_info(player_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

/*
    Stores fun facts that can be displayed to the user.
    
    Columns:
    - fact_id: The unique identifier for the fact.
    - fact: The fun fact to be displayed.
*/
CREATE TABLE fun_facts (
    fact_id SERIAL PRIMARY KEY,
    fact VARCHAR(200) NOT NULL
);


/*
 Stores information about the guesses made by users in games.

 Columns:
   - game_id: The unique identifier for the game.
   - guess: The guess made by the user.
   - guess_number: The number of the guess made by the user.
   - guess_time: The timestamp when the guess was made.
*/
CREATE TABLE guesses (
    game_id INT UNSIGNED,
    guess VARCHAR(10) NOT NULL,
    guess_number INT NOT NULL,
    guess_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id, guess_number),
    FOREIGN KEY (game_id) REFERENCES games_played(game_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);


/*
 Stores information about the items available for purchase in the shop.

 Columns:
   - item_id: The unique identifier for the item.
   - item_name: The name of the item.
   - item_cost: The cost of the item.
   - item_description: A description of the item.
   - one_time_purchase: A boolean indicating whether the item can be purchased multiple times.
*/
CREATE TABLE shop(
    item_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(50) NOT NULL,
    item_cost INT NOT NULL,
    item_description VARCHAR(500) NOT NULL,
    one_time_purchase BOOLEAN NOT NULL DEFAULT 0
);


-- TODO: make into materiailized
CREATE TABLE player_stats(
    username, 
    num_games, 
    avg_score, 
    avg_guesses, 
    avg_solve_time, 
    avg_guess_time)
AS SELECT 
    username,
    COUNT(gp.game_id),
    AVG(score),
    AVG(num_guesses),
    AVG(finish_time_sec), 
    AVG(guess_time)
    -- percentage of games won  (Getting the number of NULL finish times)
    -- Number of items used
FROM player_info AS p
JOIN games_played AS gp ON p.player_id = gp.player_id
JOIN guesses AS g ON gp.game_id = g.game_id
GROUP BY p.player_id;


/*
 Stores information about the items owned by users.

 Columns:
   - player_id: The unique identifier for the player.
   - item_id: The unique identifier for the item.
   - quantity: The quantity of the item owned by the player.
*/
CREATE TABLE player_items(
    player_id INT UNSIGNED,
    item_id INT UNSIGNED,
    quantity INT NOT NULL,
    PRIMARY KEY (player_id, item_id),
    FOREIGN KEY (player_id) REFERENCES player_info(player_id)
    ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES shop(item_id)
    ON DELETE CASCADE
);

CREATE INDEX guess_idx ON guesses (guess);