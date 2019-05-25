//  Rust program to solve a Yohaku Puzzle
// 4x4 Consecutive, sums rows/cols
//Center squares have to be triangle numbers
//From Paddy Gaunt
// May 24, 2019

const ROWS :[i32;4] = [19,15,27,11];
const COLS :[i32;4] = [39,11,3,19];
const TRIANGLES :[i32;7] = [1,3,6,10,15,21,28]; //triangle nums for this puzzle
const TRIANGLE_IX : [usize;4] = [5, 6, 9, 10];
const SIZE : usize = 16;
const X : i32 = -99; // to be ignored in grid

fn check_no_conflicts(slice : &Vec<i32>) -> bool {
	for i in 0..(slice.len()-1) {
		for j in (i+1)..slice.len() {
			if slice[i] != X && slice[j] != X && slice[i] == slice[j] {
				return false;
			}
		}
	}
	for i in 0..4 {
		let pn = &slice[TRIANGLE_IX[i]];
		if pn != &X && !TRIANGLES.contains(pn){
			return false;
		}
		//println!("{:?}", slice);
		let r = i * 4;
		if  slice[r] != X && slice[r + 1] != X && slice[r + 2] != X && slice[r + 3] != X &&
			slice[r] + slice[r + 1] + slice[r + 2] + slice[r + 3] != ROWS[i] {
			return false;
		}
		if slice[i] != X && slice[i + 4] != X && slice[i + 8] != X && slice[i + 12] != X &&
			slice[i] + slice[i + 4] + slice[i + 8] + slice[i + 12] != COLS[i] {
			return false;
		}
	}
	true
}


fn solve(values : &Vec<i32>, safe_up_to : fn(&Vec<i32>) -> bool) -> Vec<i32> { 
    let mut solution = vec![X;SIZE];

    fn extend_solution(position : usize, // increment for each position in the solution list
                       solution : &mut Vec<i32>, // list of values for solution
					   values : &Vec<i32>,
                       safe_up_to : fn(&Vec<i32>) -> bool) -> bool { // pass the function 
        for value in values.iter() {
            solution[position] = *value;
            if safe_up_to(&solution) { // i.e. this solution is good so far, push it further if not at end
                if position >= (solution.len() - 1) || extend_solution(position + 1, solution, values, safe_up_to) {
                    return true; // either got to end or extended solution OK
                }
            } else {
                solution[position] = X; // this position failed so set back to 0
                if value == &values[values.len() - 1] && position > 0 { // if at end of VALUES shift back one place as well
                    solution[position - 1] = X;
                }
                if position < (solution.len() - 1) { // set next slot to 0 next position can have an incorrect try left in it
                    solution[position + 1] = X;
                }
            }
        }
        false
    }

    if extend_solution(0, &mut solution, values, safe_up_to) { // start recursive checking from position 0
        return solution;
    }
    solution // else return whatever the last attempt was - spurious values
}

fn main() {
    let startnum : i32 = 1 + ((ROWS[0] + ROWS[1] + ROWS[2] + ROWS[3]) - 16 * (16 + 1) / 2) / 16;
    let values: Vec<i32> = (startnum..startnum + 16).collect();
	let solution = solve(&values, check_no_conflicts);
	for i in 0..4 {
		for j in 0..4 {
			print!(" {:2}", solution[i * 4 + j]);
		}
		println!("");
	}
}
