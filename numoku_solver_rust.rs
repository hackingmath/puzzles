const STARTGRID : [&str;3] = ["000800080030900500008304050070003000",
                            "250007000003007400006800700000800064",
                            "002000010600400090070006005020000500"];
const VALUES : [u32;9] = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const SIZE : usize = 36;
const N : usize = 6;

fn row_count(board : &Vec<u32>, n : usize, val : u32) -> u32 {
    //returns number of val in row n of board
    let mut tot : u32 = 0;
    for i in 0..N {
        if board[n * N + i] == val {tot += 1;}
    }
    tot
}

fn col_count(board : &Vec<u32>, n : usize, val : u32) -> u32 {
    //returns number of val in col n of board
    let mut tot : u32 = 0;
    for i in 0..N {
        if board[i * N + n] == val {tot += 1;}
    }
    tot
}

fn block_count(board : &Vec<u32>, n : usize, val : u32) -> u32 {
    //returns number of val in block n of board .. only works for 9x9
    let block : [usize;9] = match n {
        1 => [0,1,2,6,7,8,12,13,14],
        2 => [3,4,5,9,10,11,15,16,17],
        3 => [18,19,20,24,25,26,30,31,32],
        4 => [21,22,23,27,28,29,33,34,35],
        _ => [0;9]
    };
    //block.iter().fold(0, |acc, &v| acc + match board[v] - val {0  => 1, _ => 0})
    let mut tot: u32 = 0;
    for &v in block.iter() {
        if board[v] == val {
            tot += 1;
        }
    }
    tot
}

fn print_board(board : &Vec<u32>) {
    for i in 0..N {
        for j in 0..N {
            print!("{} ", board[i * N + j]);
        }
        println!("");
    }
    println!(""); // blank line between
}

fn check_no_conflicts(board : &Vec<u32>) -> bool {
    //Returns False if there ARE conflict
    for i in 0..N {
        for v in VALUES.iter() {
            if row_count(board, i, *v as u32) > 1 { // row i
                return false;
            }
            if col_count(board, i, *v as u32) > 1 { // col i
                return false;
            }
        }
    for i in 0..4 {      
        for v in VALUES.iter() {
            if block_count(board, i, *v as u32) > 1 { // block i
                return false;
            }
            }
        }
    }
    true
}

fn solve(i : usize, safe_up_to : fn(&Vec<u32>) -> bool) -> Vec<u32> { 
    let mut solution = vec![0u32;SIZE];
    let mut map_to : Vec<usize> = vec![];
    for (i, c) in STARTGRID[i].bytes().enumerate() {
        solution[i] = c as u32 - 48;
        if c == 48 { // i.e. c is '0' so this is a slot to fill
            map_to.push(i);
        }
    }
    fn extend_solution(position : usize, // increment for each position in the solution list
                       solution : &mut Vec<u32>, // list of values for solution
                       map_to : &Vec<usize>, // allows redirection of vals in solution to slots that need filling
                       safe_up_to : fn(&Vec<u32>) -> bool) -> bool { // pass the function 
        for value in VALUES.iter() {
            solution[map_to[position]] = *value;
            if safe_up_to(&solution) { // i.e. this solution is good so far, push it further if not at end
                print_board(&solution);
                if position >= map_to.len() - 1 || extend_solution(position + 1, solution, map_to, safe_up_to) {
                    return true; // either got to end or extended solution fails
                }
            } else {
                solution[map_to[position]] = 0; // this position failed so set back to 0
                if value == &VALUES[N-1] && position > 0 { // if at end of VALUES shift back one place as well
                    solution[map_to[position - 1]] = 0;
                }
                if position < (map_to.len() - 1) { // set next slot to 0 next position can have an incorrect try left in it
                    solution[map_to[position + 1]] = 0;
                }
            }
        }
        false
    }

    if extend_solution(0, &mut solution, &map_to, safe_up_to) { // start recursive checking from position 0
        return solution;
    }
    solution // else return whatever the last attempt was - spurious values
}


fn main() {
    for i in 0..STARTGRID.len() {
        let solution = solve(i, check_no_conflicts);
        print_board(&solution);
    }

}
