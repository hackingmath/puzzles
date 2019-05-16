//  Rust program to solve a Yohaku Puzzle
// 3x3 Consecutive, sums rows/cols
// May 16, 2019

extern crate rand;

use rand::{thread_rng, Rng};

const ROWS :[u8;3] = [24,16,32];
const COLS :[u8;3] = [27,19,26];

fn main() {
    let startnum = (2*(ROWS[0]+ROWS[1]+ROWS[2])/9 - 8)/2;
    
    let mut vec: Vec<u8> = (startnum..startnum+9).collect();
	let slice: &mut [u8] = &mut vec;
	loop {
		//get new slice of numbers

		thread_rng().shuffle(slice);
		if slice[0] + slice[1] + slice[2] != ROWS[0]{
			continue;
		}
		if slice[3] + slice[4] + slice[5] != ROWS[1]{
			continue;

		}
		if slice[6] + slice[7] + slice[8] != ROWS[2]{
			continue;
		}
		if slice[0] + slice[3] + slice[6] != COLS[0]{
			continue;
		}
		if slice[1] + slice[4] + slice[7] != COLS[1]{
			continue;
		}
		if slice[2] + slice[5] + slice[8] != COLS[2]{
			continue;
        }
		println!("{},{},{}",slice[0],slice[1],slice[2]);
		println!("{},{},{}",slice[3],slice[4],slice[5]);
		println!("{},{},{}",slice[6],slice[7],slice[8]);
		break
		
    }
}
