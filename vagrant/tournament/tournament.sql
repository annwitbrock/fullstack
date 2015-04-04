-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW standings;
DROP VIEW matches_played;
DROP VIEW winners;
DROP TABLE matches;
DROP TABLE players;

CREATE TABLE players ( name TEXT,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL primary key);

CREATE TABLE matches ( winner integer references players(id),
                       loser integer references players(id),
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );
                     
CREATE VIEW winners as
SELECT matches.winner as id, count(matches.winner)
FROM matches
GROUP BY matches.winner;

CREATE VIEW matches_played as
SELECT matches.winner as id, count(matches.id)
FROM matches
GROUP BY matches.id, matches.winner
UNION
SELECT matches.loser as id, count(matches.id)
FROM matches
GROUP BY matches.id, matches.loser;
                     
CREATE VIEW standings as
select m.id, m.name, m.wins, mp.count 
from (
select p.id, p.name, w.count as wins
from players p 
left join winners w on p.id = w.id
) m 
left join matches_played mp on m.id = mp.id 
order by m.wins;
