-- Your SQL goes here
CREATE TABLE match (
    id INTEGER NOT NULL,

    suspect INTEGER NOT NULL,
    victim INTEGER NOT NULL,
    
    winner INTEGER NOT NULL -- 1 if suspect won; 0 if victim won
)

CREATE TABLE moves (
    match_id INTEGER NOT NULL,

    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    side INTEGER NOT NULL,
)