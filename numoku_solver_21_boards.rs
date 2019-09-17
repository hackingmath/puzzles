extern crate time;
use time::PreciseTime;

const STARTGRID : [&str;21] = ["000800080030900500008304050070003000",
                            "250007000003007400006800700000800064",
                            "040000030085005000000600310050000070",
                            "030000000201048000000140107000000070",
                            "020000000409070200001070905000000060",
                            "000080190040007500003600050034080000",
                            "700008008100010050080040009200200006",
                            "000200000080002907304100070000008000",
                            "000040000809001030090300205000060000",
                            "700005000800036200001950009000300007",
                            "406008000300010007500010004000800402",
                            "008690200000005008307904000006006000",
                            "086000000603030002400090309000000530",
                            "080000207008000290056800000003090020",
                            "050070700006004800006100100005090020",
                            "500089060002009000000200600090180006",
                            "080200009004700060090003300600002050",
                            "002080300500070003500090007008030100",
                            "015000003002000014980000100200000480",
                            "000640700000502700007506000007053000",
                            "001000050060000307800000020080400500"];
const VALUES : [u32;9] = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const SIZE : usize = 36;
const N : usize = 6;

fn row_count(board : &Vec<u32>, n : usize, val : u32) -> u32 {
    //returns number of val in row n of board
    // this function style counting is quicker, but not for col!
    board[n*N..(n+1)*N].iter()
      .filter(|&c| *c == val).count() as u32
}

fn row_sum(board : &Vec<u32>, n : usize) -> u32 {
    //returns number of val in row n of board
    //let row: Vec<u32> = board[n*N..n*N+N].to_vec();
    //row.iter().sum::<u32>()
    //Paddy's improvement:
    board[n*N..(n+1)*N].iter().sum()
}

fn col_sum(board: &Vec<u32>,n: usize) -> u32 {
    let mut tot : u32 = 0;
    for i in 0..N {
        tot += board[i * N + n];
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

fn block_sum_count(board : &Vec<u32>, n : usize, val : u32) -> (u32, u32) {
    //returns sum and number of val in block n of board
    let block : [usize;9] = match n {
        0 => [0,1,2,6,7,8,12,13,14],
        1 => [3,4,5,9,10,11,15,16,17],
        2 => [18,19,20,24,25,26,30,31,32],
        3 => [21,22,23,27,28,29,33,34,35],
        _ => [0;9]
    };
    let mut tot: u32 = 0;
    let mut count: u32 = 0;
    for &v in block.iter() {
        if board[v] == val {
            count += 1;
        }
        tot += board[v];
    }
    (tot, count)
}

fn print_board(board : &Vec<u32>) {
    //println!("");
    for i in 0..N {
        for j in 0..N {
            print!("{} ", board[i * N + j]);
        }
        println!("");
    }
    println!(""); // blank line between
}

fn check_no_conflicts(board : &Vec<u32>) -> bool {
    //Returns False if there ARE conflicts
    for i in 0..N {
        for v in VALUES.iter() {
            if row_count(board, i, *v as u32) > 1 { // check repeats in row i
                //println!("Row count {}, {}",i,v);
                return false;
                }
            if col_count(board, i, *v as u32) > 1 { // col i
                //println!("Col count {}, {}",i,v);
                    return false;
                }
        }
        if row_count(board, i, 0) == 0 {
            
            if row_sum(board, i) != 30 {
                //println!("Row sum {}",i);
                return false;
            }
        }

        if col_count(board, i, 0) == 0 {
            if col_sum(board,i) != 30 {
                //println!("Col sum {}",i);
                return false;
            }
        }
    
    }
    for i in 0..4 {      
        for v in VALUES.iter() {
            let (_n, c) = block_sum_count(board, i, *v as u32);
            if c > 1 {
                return false;
            }
        }   

        let (n, c) = block_sum_count(board, i, 0);
        if c == 0 {
            if n != 45 {
                return false;
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
            //print_board(&solution);
            if safe_up_to(&solution) { // i.e. this solution is good so far, push it further if not at end
                if position >= map_to.len() - 1 || extend_solution(position + 1, solution, map_to, safe_up_to) {
                    return true; // either got to end or extended solution fails
                }
            } else {
                solution[map_to[position]] = 0; // this position failed so set back to 0
                if value == &VALUES[8] && position > 0 { // if at end of VALUES shift back one place as well
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
    let start_all = PreciseTime::now(); //Start of program
    for i in 0..STARTGRID.len() {
        let start = PreciseTime::now(); //Start of individual board

        let solution = solve(i, check_no_conflicts);
        println!("Board #{}:",i);
        print_board(&solution);

        let end = PreciseTime::now();
        println!("{} seconds. {} seconds total.", start.to(end),start_all.to(end));
        println!("");
    }
}
