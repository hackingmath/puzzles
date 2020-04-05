/* Numoku Solver Skyscraper Variation
July 11, 2019, JS verion 4/5/2020
https://twitter.com/1to9puzzle/status/1149354342001983494
*/

//time the program
const {performance} = require('perf_hooks');
var start = performance.now();

//board for puzzle 19192
const BOARD = [0,0,0,0,0,0,0,7,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,3,0,0,0,0,0,0,0];
//console.log(BOARD.length);

const TOP = [3,3,2,4,1,3];
const BOTTOM = [3,1,2,3,4,2];
const LEFT = [4,3,1,2,3,2]; 
const RIGHT = [2,2,4,2,2,2];

//count number of "blanks"
let numblanks = 0;
for (let i=0;i<BOARD.length;i++){
    if (BOARD[i] ==0){
        numblanks ++;
    }
}
//console.log(numblanks);

function row(board,n){
    let output = [];
    for (var i=6*n;i<6*n+6;i++){
        output.push(board[i]);
    }
    return output;
}

function col(board,n){
    let output = [];
    for (var j=0;j<6;j++){
        output.push(board[6*j+n]);
    }
    return output;
}

function quadrant(board,n){
    let quadrants = [];
    let q = [0,1,6,7]; //helper array for quadrants
    //let j1 = q.entries(); //like "enumerate"
    for (var j of q){
        let block = [];
        for (var k=0;k<3;k++){
            for (var m=6*k+3*j;m<6*k+3*j+3;m++){
                block.push(board[m]);
            }
        }
        quadrants.push(block);
    }
    return quadrants[n];
}

function populate_board(board){
  var board1 = board.slice();
    for (var i=0;i<BOARD.length;i++){
        if (BOARD[i] != 0){
            board1.splice(i,0,BOARD[i]);
        }
    }
    return board1;
}

function print_board(board){
    console.log(' ');
    var board1 = board.slice();
    if (board1.length < 36){
        board1 = populate_board(board1);
    }
    for (var i=0;i<6;i++){
        console.log((board1[6*i]).toString() +' '+(board1[6*i+1]).toString()+' '+(board1[6*i+2]).toString()+' '+(board1[6*i+3]).toString()+' '+(board1[6*i+4]).toString()+' '+(board1[6*i+5]).toString());
    }
    console.log(' ');
}

function repeat(board){
    //Returns true if there is a repeat
    //doesn't count 0's
    b1 = board.entries()
    for (b of b1){
        var count = 0;
        var num = b[1];
        if (num != 0){
            for (var i=0;i<board.length;i++){
                if (board[i] == num){
                    count ++;
                }
            }
            if (count > 1){
                return true;
            }
        }
    }
    return false;
}

function visible(myarr){
    var counter = 1;
    var highest = myarr[0];
    for (var i=1; i<6; i++){
        if (myarr[i] > highest){
            counter ++;
            highest = myarr[i];
        }
    }
    return counter;
}

function skyscraper(boardlist){
    /*Returns true if number of skyscrapers visible
    works in boardlist */
    for (var n=0;n<6;n++){
        if (visible(col(boardlist,n)) != TOP[n]){
            return false;
        }
        if (visible(row(boardlist,n)) != LEFT[n]){
            return false;
        }
        if (visible(col(boardlist,n).reverse()) != BOTTOM[n]){
            return false;
        }
        if (visible(row(boardlist,n).reverse()) != RIGHT[n]){
            return false;
        }
    }
    return true;
}

function sum(board){
    //Returns sum of given list
    var output = 0;
    for (var n of board){
        output += n;
    }
    return output;
}

function is_zero(n){
    return n == 0;
}

function check_no_conflicts(board,test){
    //returns false if there are conflicts
    // if (test == true){
    //     console.log("board1:");
    //     console.log(board1);
    // }
    var board2 = populate_board(board);
    if (test){
        print_board(board2);
    }
    
    for (var i=0;i<6;i++){
        //Check rows
        var this_row = row(board2,i);
        if (repeat(this_row)){
            if (test){
                console.log("repeat row" + i.toString())
            }
            return false;
        }
        if (sum(this_row)>30){
            return false;
        } 
        
        if (!this_row.some(is_zero)){
            if (sum(this_row)!=30){
                return false;
            }
            if (visible(this_row) != LEFT[i]){
                return false;
            }
            if (visible(this_row.reverse()) != RIGHT[i]){
                return false;
            }
        }
        //Check columns
        var this_col = col(board2,i);
        if (repeat(this_col)){
            if (test){
                console.log("repeat col" + i.toString())
            }
            return false;
        }
        if (sum(this_col)>30){
            return false;
        }

        if (!this_col.some(is_zero)){
            if (sum(this_col) !=30) {
                return false;
                }
            if (visible(this_col) != TOP[i]){
                return false;
            }
            if (visible(this_col.reverse()) != BOTTOM[i]){
                return false;
            }
        }
    }
    //Check quadrants
    for (var q=0;q<4;q++){
        var this_quadrant = quadrant(board2,q);
        if (repeat(this_quadrant)){
            if (test){
                console.log("repeat quad" + q.toString())
            }
            return false;
        }

    }
    return true;
}
let solution = [];

function solve(values, size){
    //solution = [];
    for (var i=0;i<size;i++){
        solution.push(0);
    }
    //console.log(solution);
    function extend_solution(position){
        //console.log(solution);
        //print_board(solution);
        for (var value of values){
            solution[position] = value;
            if (check_no_conflicts(solution,false)){
                if ((position >= size-1)||(extend_solution(position+1) != null)){
                    return solution;
                }
            } else {
                //
                if (values.indexOf(value) == values.length-1){
                    solution[position] = 0;
                    solution[position-1] = 0;
                }
                if (position < size-1){
                    solution[position+1] = 0;
                }
            }
        }
        return null;
    }
    return extend_solution(0);
}

 //fill test board randomly
// let tboard = [];
// for (var i=0;i<numblanks;i++){
//     tboard.push(Math.floor(10*Math.random(10)));
// }
// let newboard = populate_board(tboard)
// print_board(newboard);
// for (var r = 0;r<4;r++){
// console.log(sum(quadrant(newboard,r)));
// }

function main(){
    const NUMS = [1,2,3,4,5,6,7,8,9];
    console.log("Solution:");
    print_board(solve(NUMS,numblanks));
}

function test(){
    let solution = [];
    for (var i=0;i<numblanks;i++){
        solution.push(0);
    }
    solution[0] = 1;
    check_no_conflicts(solution,true);
}

//test();
main();

//Print time it took
var end = performance.now();
console.log("Time (secs): "+((end-start)/1000).toFixed(1).toString());