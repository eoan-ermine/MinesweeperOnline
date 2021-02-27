use diesel::{prelude::*, sqlite::SqliteConnection};
use models::{Duel, NewDuel, Move, NewMove};

pub mod models;
pub mod schema;

pub fn establish_connection() -> SqliteConnection {
    let db = "./test.sqlite3";
    SqliteConnection::establish(db).unwrap_or_else(|_| panic!("Error connection to {}", db))
}

pub fn create_duel(
    connection: &SqliteConnection,
    suspect_id: i32,
    victim_id: i32,
    suspect_side: bool,
    winner: Option<bool>,
) {
    let duel = NewDuel {
        suspect_id,
        victim_id,
        suspect_side,
        winner,
    };

    diesel::insert_into(schema::duel::table)
        .values(&duel)
        .execute(connection)
        .expect("Error inserting new duel");
}

pub fn query_duel(connection: &SqliteConnection) -> Vec<Duel> {
    schema::duel::table
        .load::<Duel>(connection)
        .expect("Error loading duels")
}

pub fn create_move(connection: &SqliteConnection, match_id: i32, info: i32) {
    let r#move = NewMove {
        match_id, info
    };
    
    diesel::insert_into(schema::moves::table)
        .values(&r#move)
        .execute(connection)
        .expect("Error inserting new move");
}

pub fn query_move(connection: &SqliteConnection) -> Vec<Move> {
    schema::moves::table
        .load::<Move>(connection)
        .expect("Error loading moves")
}