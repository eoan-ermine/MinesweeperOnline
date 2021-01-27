use super::schema::duel;

#[derive(Insertable)]
#[table_name = "duel"]
pub struct NewDuel {
    pub(crate) suspect_id: i32,
    pub(crate) victim_id: i32,

    pub(crate) suspect_side: bool,
    pub(crate) winner: Option<bool>,
}
