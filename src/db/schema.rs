table! {
    duel (id) {
        id -> Integer,
        suspect_id -> Integer,
        victim_id -> Integer,
        suspect_side -> Bool,
        winner -> Nullable<Bool>,
    }
}

table! {
    moves (id) {
        id -> Integer,
        match_id -> Integer,
        info -> Binary,
    }
}

allow_tables_to_appear_in_same_query!(duel, moves,);
