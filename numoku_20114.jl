#Solving Numoku Puzzle 20114
#https://twitter.com/1to9puzzle/status/1253318272021229568

const BOARD = Array(Int8[0,0,0,0,0,0,0,2,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,4,0,0,0,0,0,0,0])

const ROWS = [8,3,19,0,7,2]
const COLS = [0,0,9,10,7,0]
const NUMS = collect(1:9)
const NUMBLANKS = count(x->x==0,BOARD)
const output = copy(BOARD)

function populate_board(solution_board)
    #output = deepcopy(BOARD)
    copyto!(output,BOARD)
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
    ct = n:6:36
    ntuple(i->board[ct[i]],6)
end

const q = [[1,2,3,7,8,9,13,14,15],[4,5,6,10,11,12,16,17,18],[19,20,21,25,26,27,31,32,33],[22,23,24,28,29,30,34,35,36]]

function quadrant(board,n)
    qn = q[n]
    return ntuple(i->board[qn[i]],9)
end
            
function repeat(mylist)
    for n in mylist
        if n != 0 && count(x->x==n,mylist)>1
            return true
        end
    end
    return false
                
end
                
function between(arr)
    mults = [3,6,9]
    idx1 = findfirst(in(mults),arr)
    idx2 = findlast(in(mults),arr)
    if idx2 == idx1 + 1
        return 0
    end
    return sum(arr[idx1+1:idx2-1])
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

function check_no_conflicts(solution_board)
    #Returns False if there ARE conflicts
    for j in 1:6
        this_row = row(solution_board,j)
        if repeat(this_row)
            #println("repeat row",j)
            return false
        end
        if count(x->x==0,this_row) == 0 && sum(this_row) != 30
            return false
        end
        
        if (count(x->x==0,this_row) == 0) && (between(this_row) != ROWS[j])
            return false
        end
        
        this_col = col(solution_board,j)
        #println("col count 0's ",count(x->x==0,this_col))
        if repeat(this_col)
            #println("repeat col",j)
            return false
        end
        if (count(x->x==0,this_col) == 0) && (sum(this_col) != 30)
            #println("col sum",j)
            return false
        end
        
        if (count(x->x==0,this_col) == 0) && (between(this_col) != COLS[j])
            return false
        end
    end
    for i in 1:4
        this_quad = quadrant(solution_board,i)
        if repeat(this_quad)
            return false
        end
        for j in 1:9
            if count(x->x==0,this_quad) == 0 && count(x->x==j,this_quad) != 1
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
                #This change was the key. It wasn't returning the 
                #solution up to the end.
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

function main()
    soln = solve(NUMS,NUMBLANKS)
    print_board(soln)
end

@time main()
