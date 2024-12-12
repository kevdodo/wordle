# Wordle Implementation

Uses a MySQL database that connects with Python to play wordle. Written with Manuel Rodriguez for CS 121 Final Project

Our data was taken from the a csv file we found containing all the wordle words. There is one csv that is the 
is the allowed-guesses, and the other file which gives the valid solutions. The given csv is given in wordle_db. 

You should be able to run the game by running python app_client.py. 

Here are some logs that we had that might be useful

3/1 1:44 PM
    - when trying to start MySQL Database on XAMPP, need to do `sudo killall mysqld`
    to kill all current mysql servers and then do `sudo /Applications/XAMPP/xamppfiles/bin/mysql.server start` to start the mysql server
    from XAMPP.
          - https://serverfault.com/questions/480889/mysql-server-pid-file-could-not-be-found
    - Then need to start up the mysql in XAMPP which is not the normal mysql it is
    `/Applications/XAMPP/xamppfiles/bin/mysql --user=user_name --password=your_password db_name` 

    - Saw in mysql using `SELECT * FROM mysql.user` the users that were defined in
    mysql and logged in through root.

    - Messed up the normal mysql command, giving error "ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock'"
    - Possible solution is to look into installation instructions for mysql (not
    command line version, the actual one from the mysql website)
    
3/2 9:00 PM
    - Password for wordleadmin mysql user is `ilovewordle`
    - No password for wordleclient.
    
3/10 7:57 PM
    - Fixed issue of not being able to login to python application by changing
    host of each user in phpmyadmin to `localhost` rather than `%` which I
    thought meant wildcard but might not.
    - Added initial wordle game logic.
    - Gave the `wordleclient` certain permissions for accessing information in
    the database shown in wordleclient_priviledges.png

https://github.com/vinsfan368/wordle/blob/main/wordle-allowed-guesses.csv