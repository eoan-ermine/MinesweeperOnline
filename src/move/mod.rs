use std::fmt::Pointer;

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

#[derive(Debug, Clone, Copy)]
pub struct Position {
    info: u8,
}

impl Position {
    pub fn new(column: u8, row: u8) -> Self {
        Self {
            info: ((column & 0x3f) << 6) | (row & 0x3f)
        }
    }

    pub fn row(&self) -> u8 {
        self.info & 0x3f
    }

    pub fn column(&self) -> u8 {
        (self.info >> 6) & 0x3f
    }
}

impl From<u16> for Position {
    fn from(value: u16) -> Position {
        
    }
}

pub struct Move {
    info: u16,
}

impl Move {
    pub fn new(from: Position, to: Position, side: Side) -> Self {
        Self {
            info: ((side as u16 & 0xf) << 12) | ((Into::<u16>::into(from) & 0x3f) << 6) | (Into::<u16>::into(to) & 0x3f)
        }
    } 

    pub fn side(&self) -> Side {
        ((self.info >> 12) & 0x0f).into()
    }

    pub fn from(&self) -> Position {
        ((self.info >> 6) & 0x3f).into()
    }
}