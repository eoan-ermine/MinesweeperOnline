use super::schema::{duel, moves};

#[derive(Insertable)]
#[table_name = "duel"]
pub struct NewDuel {
    pub(crate) suspect_id: i32,
    pub(crate) victim_id: i32,

    pub(crate) suspect_side: bool,
    pub(crate) winner: Option<bool>,
}

#[derive(Queryable, Serialize)]
pub struct Duel {
    pub(crate) id: i32,
    pub(crate) suspect_id: i32,
    pub(crate) victim_id: i32,

    pub(crate) suspect_side: bool,
    pub(crate) winner: Option<bool>,
}

#[derive(Insertable)]
#[table_name = "moves"]
pub struct NewMove {
    pub(crate) match_id: i32,
    pub(crate) info: i32,
}

#[derive(Queryable, Serialize)]
pub struct Move {
    pub(crate) id: i32,
    pub(crate) match_id: i32,
    pub(crate) info: i32,
}