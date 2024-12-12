-- Most popular items among players
SELECT item_name, item.item_id FROM (SELECT item_id, SUM(quantity) as total_quantity
FROM player_items
GROUP BY item_id) AS item
JOIN shop ON item.item_id = shop.item_id
ORDER BY total_quantity DESC
LIMIT 1;

-- Get name, description, costs, and quantities of all items owned by a player
SELECT pi.item_id, item_name, quantity, item_cost
FROM player_items AS pi
JOIN shop AS s ON pi.item_id = s.item_id
WHERE player_id = 1;

-- Gets all the items in the shop
SELECT * FROM shop;

-- Get the number of games played by a player
SELECT authenticate('player2', 'lol');

-- Most popular items among players
SELECT item_name, item_id FROM (SELECT item_id, SUM(quantity) as total_quantity
FROM player_items
GROUP BY item_id) as quant NATURAL JOIN shop
ORDER BY total_quantity DESC
LIMIT 1;