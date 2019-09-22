//  Rust program to solve a Yohaku Puzzle
// https://twitter.com/YohakuPuzzle/status/1169939266283220992
// 4x4 Consecutive, sums rows/cols
//Center squares have to be triangle number
// Sept. 20, 2019

extern crate rand;
extern crate time;
use time::PreciseTime;

const ROWS :[i8;4] = [7,32,46,35];
const COLS :[i8;4] = [28,14,43,35];
const TRINUMS :[i8;7] = [1,3,6,10,15,21,35];
const SIZE: usize = 16;
const N: usize = 4;

const STARTNUM: usize = (2*(ROWS[0]+ROWS[1]+ROWS[2]+ROWS[3])/16 - 15)/2;

fn row_count(board : &Vec<usize>, n : usize, val : usize) -> usize {
    //returns number of val in row n of board
    // this function style counting is quicker, but not for col!
    board[n*N..(n+1)*N].iter()
      .filter(|&c| *c == val).count() as usize
}

fn board_count(board: &Vec<usize>,val: usize) -> usize {
	//returns number of times val shows up in board
	board.iter().filter(|&c| *c == val).count() as usize
}

fn row_sum(board : &Vec<usize>, n : usize) -> usize {
    //returns number of val in row n of board
    //let row: Vec<u32> = board[n*N..n*N+N].to_vec();
    //row.iter().sum::<u32>()
    //Paddy's improvement:
    board[n*N..(n+1)*N].iter().sum()
}

fn col_count(board : &Vec<usize>, n : usize, val : usize) -> usize {
    //returns number of val in col n of board
    let mut tot : usize = 0;
    for i in 0..N {
        if board[i * N + n] == val {tot += 1;}
    }
    tot
}

fn col_sum(board: &Vec<usize>,n: usize) -> usize {
    let mut tot : usize = 0;
    for i in 0..N {
        tot += board[i * N + n];
    }
    tot 
}


fn print_board(board : &Vec<usize>) {
    //println!("");
    for i in 0..N {
        for j in 0..N {
            print!("{:02} ", board[i * N + j]);
        }
        println!("");
    }
    println!(""); // blank line between
}

fn check_no_conflicts(board : &Vec<usize>,values: &Vec<usize>) -> bool {
    //Returns False if there ARE conflicts
	//first check for any repeats in board

	for v in values.iter() {
		if board_count(board, *v as usize) > 1 {
			return false;
			}
	}

	for i in 0..N {
		for v in values.iter() {
            
			if row_count(board, i, 0) == 0 {
				
				if row_sum(board, i) != ROWS[i] {
					//println!("Row sum {}",i);
					return false;
				}
			}

			if col_count(board, i, 0) == 0 {
				if col_sum(board,i) != COLS[i] {
					//println!("Col sum {}",i);
					return false;
				}
			}
		}
    }
	if !board.contains(&0) {
		if !TRINUMS.contains(&board[5]){
				return false;
			}
			if !TRINUMS.contains(&board[6]){
				return false;
			}
			if !TRINUMS.contains(&board[9]){
				return false;
			}
			if !TRINUMS.contains(&board[10]){
				return false;
			}
	}
    true
    }

fn solve(safe_up_to : fn(&Vec<usize>,&Vec<usize>) -> bool) -> Vec<usize> { 
    let mut solution = vec![0usize;SIZE];
    fn extend_solution(position : usize, // increment for each position in the solution list
                       solution : &mut Vec<usize>, // list of values for solution
                       safe_up_to : fn(&Vec<usize>,&Vec<usize>) -> bool) -> bool { // pass the function 
        let values: Vec<usize> = (STARTNUM..STARTNUM+16).collect();
		for value in values.iter() {
            solution[position] = *value;
            //print_board(&solution);
            if safe_up_to(&solution,&values) { // i.e. this solution is good so far, push it further if not at end
                if position >= 15 || extend_solution(position + 1, solution, safe_up_to) {
                    return true; // either got to end or extended solution fails
                }
            } else {
                solution[position] = 0; // this position failed so set back to 0
                if value == &values[15] && position > 0 { // if at end of VALUES shift back one place as well
                    solution[position - 1] = 0;
                }
                if position < 15 { // set next slot to 0 next position can have an incorrect try left in it
                    solution[position + 1] = 0;
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
	
	let solution = solve(check_no_conflicts);
	println!("Solution:");
	print_board(&solution);

	let end = PreciseTime::now();
	println!("{} seconds.", start.to(end));
	println!("");

}