-- Your SQL goes here
CREATE TABLE moves (
    id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    info BLOB NOT NULL,
     
    PRIMARY KEY (id)
);