// Solving a Yohaku puzzle
// May 9, 2019

extern crate rand;

use rand::{thread_rng, Rng};

const ROWS :[i32;3] = [32,60,432];
const COLS :[i32;3] = [32,36,720];

fn main() {
    let mut v: Vec<Vec<i32>> = Vec::new(); //list of lists of factors
	for i in 0..3 {
		for j in 0..3 {
			let rfacts = factor(ROWS[i]); //get factors of row product
			let cfacts = factor(COLS[j]); //get factors of col product
			let mut comb: Vec<i32> = Vec::new(); //empty list for common factors
			for f in rfacts.iter() { //go through row factors
				if cfacts.contains(f) {  //if it's in the col factors
					comb.push(*f); //put it in the comb list
				}
			}
			v.push(comb); //put common factor list in v
		}
	}

	loop {
		//println!("v: {:?}",v);
		let mut guess: Vec<i32> = Vec::new(); //empty list for factor choices
		let mut rng = rand::thread_rng();
		for flist in v.iter() { //go over every list in v
			guess.push(*rng.choose(&flist).unwrap()); //add a random choice from the list to slice
		}
	
		//get new slice of numbers

		//thread_rng().shuffle(slice);
		if guess[0] * guess[1] * guess[2] != ROWS[0]{
			continue;
		}
		if guess[3] * guess[4] * guess[5] != ROWS[1]{
			continue;

		}
		if guess[6] * guess[7] * guess[8] != ROWS[2]{
			continue;
		}
		if guess[0] * guess[3] * guess[6] != COLS[0]{
			continue;
		}
		if guess[1] * guess[4] * guess[7] != COLS[1]{
			continue;
		}
		if guess[2] * guess[5] * guess[8] != COLS[2]{
			continue;
		}
		if dupes(&guess.to_vec()){
			continue
		}
		println!("  {},{},{}",guess[0],guess[1],guess[2]);
		println!("  {},{},{}",guess[3],guess[4],guess[5]);
		println!("  {},{},{}",guess[6],guess[7],guess[8]);
		break
		}

}

fn factor(num: i32) -> std::vec::Vec<i32> {
	let mut factor_list: Vec<i32> = Vec::new(); //creates a new vector for the factors

	for i in 1..((num as f32).sqrt() as i32 + 1) {
		if num % i == 0 {
			factor_list.push(i); //pushes smallest factor to factor_list
			factor_list.push(num/i)//pushes largest factor to factor_list
		}
	}
	factor_list.sort(); // sorts factors in numerical order
	factor_list //returns the list of factors
}

// Function to make sure there are no duplicated values in the solution list
fn dupes(list : &Vec<i32>) -> bool {
	for element in list.iter(){
		if list.iter().filter(|&n| *n == *element).count() > 1 {
			return true;
		}
	}
	false
}