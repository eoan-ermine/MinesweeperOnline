use diesel::{prelude::*, sqlite::SqliteConnection};
use models::NewDuel;

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
