-- Your SQL goes here
CREATE TABLE duel (
    id INTEGER NOT NULL,

    suspect_id INTEGER NOT NULL,
    victim_id INTEGER NOT NULL,
    
    suspect_side BOOLEAN NOT NULL,

    winner BOOLEAN, -- 1 if suspect won; 0 if victim won
    PRIMARY KEY (id)
);