#![feature(proc_macro_hygiene, decl_macro)]

use minesweeper_online::db::{establish_connection, query_duel, models::{Duel, Move}};
use rocket_contrib::json::Json;

#[macro_use]
extern crate rocket;
#[macro_use]
extern crate rocket_contrib;
#[macro_use]
extern crate serde;

#[derive(Serialize)]
struct DuelsJsonResponse {
    data: Vec<Duel>,
}

#[derive(Serialize)]
struct MovesJsonResponse {
    data: Vec<Move>,
}

#[get("/duels")]
fn duels_get() -> Json<DuelsJsonResponse> {
    let mut response = DuelsJsonResponse { data: vec![] };

    let conn = establish_connection();
    for duel in query_duel(&conn) {
        response.data.push(duel);
    }
    Json(response)
}



fn main() {
    rocket::ignite()
        .mount("/", routes![duels_get])
        .launch();
}