
    return false
    end

function print_board(solution_board)
    print()
    for i in 1:9
        for j in 1:9
            print(' ')
            print(solution_board[i, j])
        end
        println()
    end
    println() #blank line
end

function consecutives(arr)
    #returns true if there are consecutive nums in arr
    for i in 1:8
        if arr[i] != 0 && arr[i+1] != 0
            if (arr[i+1]-arr[i]) in [1,-1]
                return true
            end
        end
    end
    return false
end

function sum_consecutives(arr)
    if !consecutives(arr)
        return 0
    end
    output = 0
    for i in 1:8
        if (arr[i+1]-arr[i]) in [1,-1]
            output += (arr[i+1]+arr[i])
            return output
        end
        output += arr[i]
    end
    output
end

function check_no_conflicts(board)
    for i in 1:9
        thisrow = view(board,i,:)
        if repeat(thisrow)
            return false
        end
        
#         if consecutives(thisrow) && LEFT[i] == 0
#             return false
#         end
        
#         if consecutives(reverse(thisrow)) && RIGHT[i] == 0
#             return false
#         end
        
#         if sum_consecutives(thisrow) > LEFT[i]
#             return false
#         end
        
#         if count(j->j==0,thisrow) == 0
#             if sum_consecutives(reverse(thisrow)) > RIGHT[i]
#                 return false
#             end
#         end
        
        if consecutives(thisrow)
            if sum_consecutives(thisrow) != LEFT[i]
                return false
            end
        end
        
        if count(j->j==0,thisrow) == 0 
            if sum_consecutives(thisrow) != LEFT[i]
                return false
            end
            if sum_consecutives(reverse(thisrow)) != RIGHT[i]
                return false
            end
        end
        
        thiscol = view(board, :, i)
        if repeat(thiscol)
            return false
        end
        
#         if consecutives(thiscol) && TOP[i] == 0
#             return false
#         end
        
#         if consecutives(reverse(thiscol)) && BOTTOM[i] == 0
#             return false
#         end
        
#         if sum_consecutives(thiscol) > TOP[i]
#             return false
#         end
        
#         if count(j->j==0,thiscol) == 0
#             if sum_consecutives(reverse(thiscol)) > BOTTOM[i]
#                 return false
#             end
#         end
        
        if consecutives(thiscol)
            if sum_consecutives(thiscol) != TOP[i]
                return false
            end
        end
        
        if count(j->j==0,thiscol) == 0
            if sum_consecutives(thiscol) != TOP[i]
                return false
            end
            if sum_consecutives(reverse(thiscol)) != BOTTOM[i]
                return false
            end
        end
        
        if repeat(quadrant(board,i))
            return false
        end
    end
    return true
end

function solve(values, safe_up_to, size)
    solution_list = zeros(size)
    ind = 1
    for r in 1:9
        for c in 1:9
            if  BOARD[r, c] == 0
                lookup[ind] = CartesianIndex(r, c)
                ind += 1
            end
        end
    end
    function extend_solution(position)
        for value in values
             BOARD[lookup[position]] = value
            #println(BOARD)
            if safe_up_to(BOARD)
                if position >= size
                    return true
                end
                new_solution = extend_solution(position+1)
                if new_solution
                    return true
                end
            else
                 BOARD[lookup[position]] = 0
                if value == values[length(values)] && position > 1
                     BOARD[lookup[position-1]] = 0
                end
                if position < size
                     BOARD[lookup[position+1]] = 0
                end
            end
        end
        false
    end
    extend_solution(1)
end

function main()
    #b = BOARD
        
    blanks = count(i->(i==0),BOARD)
    #print("blanks:",blanks)
    if solve(1:9, check_no_conflicts, blanks)
        print_board(BOARD)
    else
        print("solve failed to find solution")
    end
end

@time main()

#=
Solution:
 3 4 5 6 2 8 1 9 7
 9 8 1 5 4 7 6 2 3
 7 6 2 3 9 1 5 4 8
 6 9 4 1 5 3 8 7 2
 5 7 3 2 8 9 4 1 6
 1 2 8 7 6 4 9 3 5
 2 5 7 9 1 6 3 8 4
 4 1 6 8 3 2 7 5 9
 8 3 9 4 7 5 2 6 1

50.647787 seconds (1.02 G allocations: 84.545 GiB, 13.48% gc time)
=#
