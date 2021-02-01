#[repr(u16)]
#[derive(Debug, Clone, Copy)]
pub enum Side {
    WHITE = 0,
    BLACK = 1,
}

impl From<u16> for Side {
    fn from(value: u16) -> Self {
        match value {
            0 => Side::WHITE,
            1 => Side::BLACK,
            _ => unreachable!(),
        }
    }
}

impl Into<u16> for Side {
    fn into(self) -> u16 {
        match self {
            Side::WHITE => 0,
            Side::BLACK => 1,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Position {
    info: u8,
}

pub trait PosEncoder {
    fn encode_row(row: u8) -> u8;
    fn encode_column(column: u8) -> u8;
}

impl PosEncoder for Position {
    fn encode_row(row: u8) -> u8 {
        row & 0x3f
    }
    fn encode_column(column: u8) -> u8 {
        (column & 0x3f) << 6
    }
}

pub trait PosDecoder {
    fn decode_row(data: u8) -> u8;
    fn decode_column(data: u8) -> u8;
}

impl PosDecoder for Position {
    fn decode_row(data: u8) -> u8 {
        data & 0x3f
    }
    fn decode_column(data: u8) -> u8 {
        (data >> 6) & 0x3f
    }
}

impl Position {
    pub fn new(column: u8, row: u8) -> Self {
        Self {
            info: Self::encode_column(column) | Self::encode_row(row)
        }
    }
    pub fn row(&self) -> u8 {
        Self::decode_row(self.info)
    }
    pub fn column(&self) -> u8 {
        Self::decode_column(self.info)
    }
}

impl From<u16> for Position {
    fn from(value: u16) -> Self {
        let value = value as u8;
        Self::new(Self::decode_column(value), Self::decode_row(value))
    }
}

impl Into<u16> for Position {
    fn into(self) -> u16 {
        self.info as u16
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Move {
    info: u16,
}

trait MoveEncoder {
    fn encode_from(from: Position) -> u16;
    fn encode_to(to: Position) -> u16;
    fn encode_side(side: Side) -> u16;
}

impl MoveEncoder for Move {
    fn encode_from(from: Position) -> u16 {
        (Into::<u16>::into(from) & 0x3f) << 6
    }
    fn encode_to(to: Position) -> u16 {
        Into::<u16>::into(to) & 0x3f
    }
    fn encode_side(side: Side) -> u16 {
        (side as u16 & 0xf) << 12
    }
}

trait MoveDecoder {
    fn decode_from(data: u16) -> Position;
    fn decode_to(data: u16) -> Position;
    fn decode_side(data: u16) -> Side;
}

impl MoveDecoder for Move {
    fn decode_from(data: u16) -> Position {
        ((data >> 6) & 0x3f).into()
    }
    fn decode_to(data: u16) -> Position {
        (data & 0x3f).into()
    }
    fn decode_side(data: u16) -> Side {
        ((data >> 12) & 0xf).into()
    }
}


impl Move {
    pub fn new(from: Position, to: Position, side: Side) -> Self {
        Self {
            info: Self::encode_side(side) | Self::encode_from(from) | Self::encode_to(to)
        }
    } 

    pub fn side(&self) -> Side {
        Self::decode_side(self.info)
    }

    pub fn from(&self) -> Position {
        Self::decode_from(self.info)
    }

    pub fn to(&self) -> Position {
        Self::decode_to(self.info)
    }
}

impl From<u16> for Move {
    fn from(value: u16) -> Self {
        Self::new(Self::decode_from(value), Self::decode_to(value), Self::decode_side(value))
    }
}

#[cfg(test)]
mod tests {
    use super::Position;

    #[test]
    fn test_position() {
        use super::*;
        
        let position = Position::new(0, 0);
        
        let value: u16 = position.into();
        let new_position = value.into();

        assert_eq!(position, new_position);
        assert!(new_position.row() == 0 && new_position.column() == 0)
    }
    #[test]
    fn test_move() {
        use super::*;

        let from_position = Position::new(0, 1);
        let to_position = Position::new(5, 3);
        let side = Side::WHITE;

        let player_move = Move::new(from_position, to_position, side);
        assert_eq!(player_move.to(), Position::new(5, 3));
    }
}