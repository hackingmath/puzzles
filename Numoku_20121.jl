#Puzzle 20121
#https://twitter.com/1to9puzzle/status/1255848687298740224
const BOARD = Array(Int8[0,0,0,0,0,0,0,5,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,2,0,0,0,0,0,0,0])
const ROWS = [[2,3],[4,6],[],[2,3,4,6],[2,5,6],[2,6]]
const COLS = [[2,6],[],[2,6],[2,3,4],[3,5],[6]]
#for quadrants function
const q = [[1,2,3,7,8,9,13,14,15],[4,5,6,10,11,12,16,17,18],[19,20,21,25,26,27,31,32,33],[22,23,24,28,29,30,34,35,36]]
const NUMS = 1:9
const NUMBLANKS = count(i->i==0,BOARD)
#print(NUMBLANKS) 

const output = copy(BOARD)

function populate_board(solution_board)
    copyto!(output, BOARD)
    ind = 1
    for i in 1:36
        if output[i] == 0
            output[i] = solution_board[ind]
            ind +=1
        end
    end
    output
end

function row(board,n)
    #returns values in row n of board
    return @view board[6*n-5:6*n]
end

function col(board,n)
    #returns values in col n of board
        #ct = n:6:36
        ntuple(i->board[6*(i-1)+n], 6)
end

function quadrant(board,n)
    return ntuple(i->board[q[n]][i],9)
end
                
function repeat(mylist)
    for n in mylist
        if n != 0 && count(i->i==n,mylist)>1
            return true
        end
    end
    return false
                
end
                                

function print_board(solution_board)
    #board = populate_board(solution_board)

    print()
    for i in 1:36
        if i % 6 == 0
            println(solution_board[i])
        else
            print(solution_board[i])
            print(' ')
        end
    end
    println() #blank line
end

# function split_array(arr,ind)
#     sum1 = sum(arr[1:ind-1])
#     sum2 = sum(arr[ind:6])
#     return sum1,sum2
# end

function is_factor_or_multiple(a,b)
    if (mod(a,b) == 0) || (mod(b,a) == 0)
        return true
    end
    return false
end
                            
function check_no_conflicts(solution_board)
    #Returns false if there ARE conflicts
    for j in 1:6
        this_row = row(solution_board,j)
        if repeat(this_row)
            #println("repeat row",j)
            return false
        end

        for b in ROWS[j]
            if count(i->i==0, this_row[1:(b-1)]) == 0
                #c = sum(this_row[1:(b-1)])
                if sum(this_row[1:(b-1)]) >= 30 || sum(this_row[1:(b-1)]) == 0
                    return false
                end
                if !is_factor_or_multiple(sum(this_row[1:(b-1)]), 30-sum(this_row[1:(b-1)]))
                    return false
                end
            end
        end

        if count(i->i==0,this_row) == 0
            if sum(this_row) != 30
                return false
            end
        end

        this_col = col(solution_board,j)

        if repeat(this_col)
            #println("repeat col",j)
            return false
        end
        for b in COLS[j]
            if count(i->i==0, this_col[1:(b-1)]) == 0
                #c = sum(this_col[1:(b-1)])
                if sum(this_col[1:(b-1)]) >= 30 || sum(this_col[1:(b-1)]) == 0
                    return false
                end
                if !is_factor_or_multiple(sum(this_col[1:(b-1)]), 30-sum(this_col[1:(b-1)]))
                    return false
                end
            end
        end
        if count(i->i==0,this_col) == 0
            if sum(this_col) != 30
                #println("col sum",j)
                return false
            end
        end
    end
    for i in 1:4
        #this_quad = quadrant(solution_board,i)
        if repeat(quadrant(solution_board,i))
            return false
        end
        for j in 1:9
            if count(i->i==0,quadrant(solution_board,i)) == 0 && count(i->i==j,quadrant(solution_board,i)) != 1
                #println("quad",n)
                return false
            end
        end
    end

    return true
end

function solve(values, size)
    solution_list = zeros(size)

    function extend_solution(position)
        for value in values
            solution_list[position] = value
            solution = populate_board(solution_list)
            #print_board(solution)
            if check_no_conflicts(solution)
                if position >= size
                    return solution
                end
                new_solution = extend_solution(position+1)
                if new_solution != nothing
                    return new_solution
                end
            else
                solution_list[position] = 0
                if position < size
                    solution_list[position+1] = 0
                end
                if value == values[length(values)]
                    #println("end of values")
                    if position > 1
                        solution_list[position-1] = 0
                    end
                end
                
            end
        end
        nothing
    end
    extend_solution(1)
end
                
# function test()
#     board1 = rand(1:9,32)
#     newboard = populate_board(board1)
#     print_board(newboard)
#     end

function main()
    soln = solve(NUMS,NUMBLANKS)
    print_board(soln)
end

@time main()
