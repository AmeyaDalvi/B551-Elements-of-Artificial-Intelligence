import pdb

board = [' '*15]*5+['x'+' '*14]+['xxxxx'+' '*10]
piece = [ "xxxx", "  x " ]
piece2 = [ "xxxx", "   x" ]


def combine(str1, str2):
    return "".join([ c if c != " " else str2[i] for (i, c) in enumerate(str1) ] )

def place_piece(board, piece, row, col):
    # if not col+len(piece[0])>=len(board[0]):
        return board[0:row] + \
                [ (board[i+row][0:col] + combine(r, board[i+row][col:col+len(r)]) + board[i+row][col+len(r):] ) for (i, r) in enumerate(piece) ] + \
                board[row+len(piece):]
    # else:
    #     print("in else")
    #     return board[0:row] + \
    #             [ (board[i+row][0:col] + combine(r, board[i+row][col:col+len(r)]) ) for (i, r) in enumerate(piece) ] + \
    #             board[row+len(piece):]


def check_collision(board, piece, row, col):
    return col+len(piece[0]) > len(board[0]) or row+len(piece) > len(board) \
        or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ] )

def move(state, piece,row, col, col_offset=1):
    new_col = max(0, min(len(state[0]) - len(piece[0]), col + col_offset))
    (piece, col) = (piece, new_col) if not check_collision(state, piece, row, new_col) else (piece, col)

    return (row,col)

def down(state,piece,row,col):
    while not check_collision(state, piece, row+1, col):
      row += 1
    return (row,col)



# print(succ(board,piece))

def rotate_piece(piece, rotation):
    rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
    return { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }[rotation]

def hflip_piece(piece):
    return [ str[::-1] for str in piece ]

def vflip_piece(piece):
    return [ str for str in piece[::-1] ]


def transform(piece):
    plus  = [ " x ", "xxx", " x "]
    all_piece = []
    if piece == plus:
        all_piece.append((piece,''))
    else:      
        all_piece.append((piece,False))

        rot = rotate_piece(piece,90)
        all_piece.append((rot,'n'))

        b = rotate_piece(rot,90)
        all_piece.append((b,'nn'))

        c = rotate_piece(b,90)
        all_piece.append((c,'nnn'))

        d = hflip_piece(piece)
        all_piece.append((d,'h'))

        e = hflip_piece(rot)
        all_piece.append((e,'nh'))

        f = hflip_piece(b)
        all_piece.append((f,'hnn'))

        g = rotate_piece(d,90)
        all_piece.append((g,'hn'))

    return all_piece

def left_right(best_suc,piece,r,c):
    pass




# for i in transform(piece):
#     print("|\n".join(i[0]) + "|\n" + "-" * len(i[0][0]))
#     print('Transformations: ',i[1])

# def all_succ(state,piece):
#     return [succ(state,p) for p in transform(piece)]


    
# def agg_height(board):
#         height=0
#         for row in range(len(board)-1,-1,-1):
#             for col in range(len(board[0])):
#                 if row> 0:
#                     if board[row][col] == 'x':
#                         height+=1
#                     elif board[row][col] == ' ' and board[row-1][col] == 'x':
#                         height+=1

#                     else:
#                         continue
#         return height

def agg_height(board):
    height=0
    for col in range(len(board[0])):
        for row in range(len(board)-1,-1,-1):
            if row> 0:
                if board[row][col] == 'x':
                    height+=1
                elif board[row][col] == ' ' and board[row-1][col] == 'x':
                    height+=1
                else:
                    continue
    return height

def comp_lines(board):
    line_count=0
    for row in range(len(board)-1,-1,-1):
        if board[row].count('x') == len(board[row]):
            line_count+=1
        else:
            continue
    return line_count

def holes(board):
    holes=0
    for col in range(len(board[0])):
        block = False
        for row in range(len(board)):
            if board[row][col] != ' ':
                block = True
            elif board[row][col] == ' ' and block:
                holes+=1
    return holes

# def bumpiness(board):
#     bump=0
#     for row in range(len(board)-1,-1,-1):
#         height1=0
#         height2=0
#         for col in (len(board[0])):
#             if board[col][row] == 'x':
#                 height1+=1
#             if row !=0:
#                 if board[col][row-1] == 'x':
#                     height2+=1
#         bump += abs(height1-height2)
#     return bump

def bumpiness(board):
    bump=0
    for col in range(len(board[0])):
        height1=0
        height2=0
        for row in range(len(board)-1,-1,-1):
            if board[row][col] == 'x':
                height1+=1
            if row !=0:
                if board[row-1][col] == 'x':
                    height2+=1
        bump += abs(height1-height2)
    return bump


def heuristic(state):
    # return 50*comp_lines(state)-10*(holes(state))-5*(agg_height(state))-2*(bumpiness(state))
    # print(state)
    return 0.76*comp_lines(state)-0.35*(holes(state))-0.51*(agg_height(state))-0.18*(bumpiness(state))


def max_height(board):
    # print(board)
    max_height=[]
    for col in range(len(board[0])):
        height=0
        for row in range(len(board)-1,-1,-1):
            if row> 0:
                if board[row][col] == 'x':
                    height+=1
                elif board[row][col] == ' ' and board[row-1][col] == 'x':
                    height+=1
                else:
                    continue
        max_height.append(height)
    return max(max_height)

def succ(state,piece,transformation):
    suc = {}
    for i in range(len(state[0])-len(piece)-1):
        r,c=down(state,piece,0,i)
        temp_suc = place_piece(state,piece,r,c)
        suc[tuple(temp_suc,)]=[(r,c),transformation,heuristic(temp_suc)]
    return suc


def all_succ(state,piece):
    final_succ_list = {}
    for p,t in transform(piece):
        temp_suc_dict = succ(state,p,t)
        for k in temp_suc_dict.keys():
            final_succ_list[k] = temp_suc_dict[k]
    return final_succ_list

# heuristic_1 = [heuristic(p) for p in all_succ(board,piece)]
#best = all_succ(board,piece)[all_heuristic.index(max(all_heuristic))]
#print("|\n".join(best) + "|\n" + "-" * len(best[0]))

test_succ = all_succ(board,piece)
print(len(test_succ))

# for i in test_succ.items():
#     print(i)

def best_succ(all_succ_dict):
    max_heuristic = -100000
    for i in all_succ_dict.items():
        if i[1][2]>max_heuristic:
            max_heuristic=i[1][2]
            best_suc = i #best suc is a tuple with first value as the state and second value as [pos,transformation,heuristic]
    return best_suc

# print(best_succ(test_succ))
best_suc = best_succ(test_succ)
print("|\n".join(best_suc[0]) + "|\n" + "-" * len(best_suc[0][0]))
# for row in best_suc[0]:
#     print(*row)
print(" position: " ,best_suc[1][0], " transformation: ", best_suc[1][1], " heuristic: ", best_suc[1][2])
