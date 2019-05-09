// First Rust program to solve a 1 to 9 Puzzle
// May 9, 2019

extern crate rand;

use rand::{thread_rng, Rng};

const ROWS :[u8;3] = [16,18,11];
const COLS :[u8;3] = [8,18,19];
const DIAGS :[u8;2] = [16,20]; //up,down

fn main() {
    let mut vec: Vec<u8> = (1..9).collect(); //9 is left out of today's puzzle
	let slice: &mut [u8] = &mut vec;
	loop {
		//get new slice of numbers

		thread_rng().shuffle(slice);
		if slice[0] + slice[1] + slice[2] != ROWS[0]{
			continue;
		}
		if slice[3] + 9 + slice[4] != ROWS[1]{
			continue;

		}
		if slice[5] + slice[6] + slice[7] != ROWS[2]{
			continue;
		}
		if slice[0] + slice[3] + slice[5] != COLS[0]{
			continue;
		}
		if slice[1] + 9 + slice[6] != COLS[1]{
			continue;
		}
		if slice[2] + slice[4] + slice[7] != COLS[2]{
			continue;
		}
		if slice[5] + 9 + slice[2] != DIAGS[0]{
			continue;
		}
		if slice[0] + 9 + slice[7] != DIAGS[1]{
			continue;
		}
		println!("{},{},{}",slice[0],slice[1],slice[2]);
		println!("{},{},{}",slice[3],9,slice[4]);
		println!("{},{},{}",slice[5],slice[6],slice[7]);
		break
		}

}