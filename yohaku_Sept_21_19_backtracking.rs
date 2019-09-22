//  Rust program to solve a Yohaku Puzzle
// https://twitter.com/YohakuPuzzle/status/1175398323634786304
// 5x5 Consecutive, sums rows/cols
//Center squares have to be primes
// Sept. 20, 2019

extern crate rand;
extern crate time;
use time::PreciseTime;

const ROWS :[isize;5] = [52,37,90,62,34];
const COLS :[isize;5] = [57,9,63,91,55];
const PRIMES :[isize;11] = [2,3,5,7,11,13,17,19,23,29,31];
const SIZE: isize = 25;
const N: isize = 5;
const DEFAULT_NUM: isize = 30;

//const STARTNUM: isize = (2*(ROWS[0]+ROWS[1]+ROWS[2]+ROWS[3]+ROWS[4])/25 - 24)/2;
const STARTNUM: isize = (ROWS[0]+ROWS[1]+ROWS[2]+ROWS[3]+ROWS[4])/SIZE - (SIZE-1)/2;

fn row_count(board : &Vec<isize>, n : isize, val : isize) -> usize {
    //returns number of val in row n of board
    // this function style counting is quicker, but not for col!
    let startn: usize = (n*N) as usize;
    let endn: usize = ((n+1)*N) as usize;
    board[startn..endn].iter()
      .filter(|&c| *c == val).count()
}

fn board_count(board: &Vec<isize>,val: isize) -> isize {
	//returns number of times val shows up in board
	board.iter().filter(|&c| *c == val).count() as isize
}

fn row_sum(board : &Vec<isize>, n : isize) -> isize {
    //returns number of val in row n of board
    let startn: usize = (n*N) as usize;
    let endn: usize = ((n+1)*N) as usize;
    let row: Vec<isize> = board[startn..endn].to_vec();
    let mut output :isize = 0;
    for num in row.iter() {
        if num != &DEFAULT_NUM {
            output += num;
        }
    }
    output
    //row.iter().sum::<u32>()
    //Paddy's improvement:
    
    //board[startn..endn].iter().sum()
    
}

fn col_count(board : &Vec<isize>, n : isize, val : isize) -> isize {
    //returns number of val in col n of board
    let mut tot : isize = 0;
    for i in 0..N {
        let idx = (i * N + n) as usize;
        if board[idx] == val {tot += 1;}
    }
    tot
}

fn col_sum(board: &Vec<isize>,n: isize) -> isize {
    let mut tot : isize = 0;
    for i in 0..N {
        let idx = (i * N + n) as usize;
        if board[idx] != 30 {
            tot += board[idx];
        }
    }
    tot 
}


fn print_board(board : &Vec<isize>) {
    //println!("");
    for i in 0..N {
        for j in 0..N {
            let idx = (i * N + j) as usize;
            print!("{} ", board[idx]);
        }
        println!("");
    }
    println!(""); // blank line between
}

fn check_no_conflicts(board : &Vec<isize>,values: &Vec<isize>) -> bool {
    //Returns false if there ARE conflicts
	//first check for any repeats in board
    for v in values.iter() {
		if *v != DEFAULT_NUM && board_count(board, *v as isize) > 1 {
			return false;
			}
	}
    
    for i in 0..N {
        let newi = i as isize;
        if row_sum(board, newi) - 1 > ROWS[i as usize]{ 
            return false;
        }
        if row_count(board, newi, DEFAULT_NUM) == 0 {
            if row_sum(board, newi) != ROWS[i as usize] {
                return false
            }
        }
        if col_sum(board, i) - 1 > COLS[i as usize] {
            return false;
        }
        if col_count(board, i, DEFAULT_NUM) == 0 {
            if col_sum(board, i) != COLS[i as usize] {
                return false
            }
        }
    }

	

	if !board.contains(&DEFAULT_NUM) {
		if !PRIMES.contains(&board[6]){
				return false;
			}
			if !PRIMES.contains(&board[7]){
				return false;
			}
			if !PRIMES.contains(&board[8]){
				return false;
			}
			if !PRIMES.contains(&board[11]){
				return false;
			}
            if !PRIMES.contains(&board[12]){
				return false;
			}
            if !PRIMES.contains(&board[13]){
				return false;
			}
            if !PRIMES.contains(&board[16]){
				return false;
			}
            if !PRIMES.contains(&board[17]){
				return false;
			}
            if !PRIMES.contains(&board[18]){
				return false;
			}
	}
    true
    }

fn solve(safe_up_to : fn(&Vec<isize>,&Vec<isize>) -> bool) -> Vec<isize> { 
    let mut solution = vec![30isize;SIZE as usize];
    fn extend_solution(position : isize, // increment for each position in the solution list
                       solution : &mut Vec<isize>, // list of values for solution
                       safe_up_to : fn(&Vec<isize>,&Vec<isize>) -> bool) -> bool { // pass the function 
        let values: Vec<isize> = (STARTNUM..STARTNUM+SIZE).collect();
		for value in values.iter() {
            solution[position as usize] = *value as isize;
            //print_board(&solution);
            if safe_up_to(solution,&values) { // i.e. this solution is good so far, push it further if not at end
                if position >= 24 || extend_solution(position + 1, solution, safe_up_to) {
                    return true; // either got to end or extended solution fails
                }
            } else {
                solution[position as usize] = 30; // this position failed so set back to 0
                if value == &values[24] && position > 0 { // if at end of VALUES shift back one place as well
                    solution[position as usize - 1] = 30;
                }
                if position < 24 { // set next slot to 0 next position can have an incorrect try left in it
                    solution[position as usize + 1] = 30;
                }
            }
        }
        false
    }

    if extend_solution(0, &mut solution, safe_up_to) { // start recursive checking from position 0
        return solution;
    }
    solution // else return whatever the last attempt was - spurious values
}


fn main() {

	let start = PreciseTime::now();
	//println!("startnum: {}",STARTNUM);
	let solution = solve(check_no_conflicts);
	println!("Solution:");
	print_board(&solution);

	let end = PreciseTime::now();
	println!("{} seconds.", start.to(end));
	println!("");

}