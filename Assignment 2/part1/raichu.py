#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def string_to_board(board,N):
    boardList = []
    for i in range(0,len(board),N):
        boardList.append([ char for char in board[i:i+N]])
    # for row in boardList:
    #     print(*row)
    return boardList

def pichu_count(board, pichu, row, col):
    top_right = 0
    top_left = 0
    bottom_right = 0
    bottom_left =0
    
    if pichu == 'b':
        jump_flag = False
        count = 0
        for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):  # top-left diagonal
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                top_left += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                top_left +=2
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        jump_flag = False
        count = 0
        for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))): # top-right diagonal
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                top_right += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                top_right +=2
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        return top_left + top_right

            
    if pichu =='w':
        jump_flag = False
        count = 0
        for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)): #bottom-left diagonal
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                bottom_left += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                bottom_left +=2
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
            
        jump_flag = False
        count = 0
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))): # bottom-right diagonal
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                bottom_right += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                bottom_right +=2
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
        
        return  bottom_left + bottom_right          
                

def pikachu_count(board, pikachu, row, col):
    top = 0
    bottom = 0
    left = 0
    right = 0

    jump_flag = False
    count = 0

    if pikachu == 'B':
        jump_flag = False
        count = 0
        
        for i in range(row-1,-1,-1): # top direction
            k= i
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and count ==3):
                break

            if (jump_flag == True and top ==0 and count ==2):
                break

            if (board[i][col] == '.' and jump_flag == False):
                top +=1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                if top == 0:
                    top += 2
                elif top == 2:
                    top +=1 
                count +=1
            elif (board[i][col] in 'wW'):
                if jump_flag == False: 
                    jump_flag = True
                count += 1
            elif (board[i][col] in 'B@$'):
                break
       

    if pikachu == 'W':
        jump_flag = False
        count = 0
        for i in range(row+1,len(board)): # bottom direction
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and  count ==3):
                break
            if (jump_flag == True and bottom ==0 and count ==2):
                break
            

            if (board[i][col] == '.' and jump_flag == False):
                bottom +=1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                if bottom == 0:
                    bottom += 2
                elif bottom == 2:
                    bottom +=1
                count +=1
            elif (board[i][col] in 'bB'):
                if jump_flag == False: 
                    jump_flag = True
                count += 1
            elif (board[i][col] in 'W@$'):
                break
    

    jump_flag = False
    count = 0
    for i in range(col-1,-1,-1): # left direction
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and count ==3):
            break
        if (jump_flag == True and left ==0 and count ==2):
                break

        if (board[row][i] == '.' and jump_flag == False):
            left +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            if left == 0:
                left += 2
            elif left == 2:
                left +=1 
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag = True
            count += 1
        elif (pikachu =='W' and board[row][i] in 'W@$') or (pikachu =='B' and board[row][i] in 'B@$'):
                break

    jump_flag = False
    count = 0
    for i in range(col+1,len(board[0])): # right direction
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and  count ==3):
            break
        if (jump_flag == True and right ==0 and count ==2):
                break

        if (board[row][i] == '.' and jump_flag == False):
            right +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            if right == 0:
                right += 2
            elif right == 2:
                right +=1 
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag = True
            count += 1
        elif (pikachu =='W' and board[row][i] in 'W@$') or (pikachu =='B' and board[row][i] in 'B@$'):
                break
    
    if pikachu == 'B':
        return top + left + right
    elif pikachu == 'W':
        return bottom +left + right

def raichu_count(board, raichu, row, col):
    top = bottom = left = right = top_left = top_right = bottom_left = bottom_right = 0

    jump_flag = False
    jump_count = 0
    for i in range(row-1,-1,-1):  # top direction
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                top += 1
            elif (jump_flag == True and jump_count == 0):
                top += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top += 1
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i in range(row+1,len(board)): # bottom direction
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom += 1
            elif (jump_flag == True and jump_count == 0):
                bottom += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom += 1
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i in range(col-1,-1,-1): # left direction
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                left += 1
            elif (jump_flag == True and jump_count == 0):
                left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                left += 1
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[row][i] in '@wW') or (raichu == '$' and board[row][i] in '$bB')):
            break

        
    jump_flag = False
    jump_count = 0
    for i in range(col+1,len(board[0])): #right direction
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                right += 1
            elif (jump_flag == True and jump_count == 0):
                right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                right += 1
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[row][i] in '@wW') or (raichu == '$' and board[row][i] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)): # top-left diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                top_left += 1
            elif (jump_flag == True and jump_count == 0):
                top_left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))): # top-right diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                top_right += 1
            elif (jump_flag == True and jump_count == 0):
                top_right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)): # bottom-left diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom_left += 1
            elif (jump_flag == True and jump_count == 0):
                bottom_left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))): # bottom-right diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom_right += 1
            elif (jump_flag == True and jump_count == 0):
                bottom_right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    return top + bottom + left + right + top_left + top_right + bottom_left + bottom_right

def heuristic1(board):
    nw = sum(row.count('w') for row in board)
    nb = sum(row.count('b') for row in board)
    nW = sum(row.count('W') for row in board)
    nB = sum(row.count('B') for row in board)
    nWR = sum(row.count('@') for row in board)
    nBR = sum(row.count('$') for row in board)
    return (2*(nw - nb) + 3*(nW - nB) + 8*(nWR - nBR))


def heuristic2(board):
   
    wp=0
    wP=0
    bp=0
    bP=0    
    N = len(board)
   
    for i in range(N):
        for j in range(N):

            if board[i][j]=='w':
                wp += math.floor(N/2) - math.ceil((N-i-1)/2) +1
            elif board[i][j]=='b':
                bp += math.floor(N/2) - math.ceil(i/2) +1
            elif board[i][j]=='W':
                wP += math.ceil(N/3) - math.ceil((N-i-1)/3) +1
            elif board[i][j]=='B':
                bP += math.ceil(N/3) - math.ceil(i/3) +1
   
    return (wp+wP-bp-bP)

def heuristic3(board):
    black_count = 0
    white_count = 0

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'w':
                white_count += pichu_count(board,board[row][col], row, col)
            elif board[row][col] == 'b':
                black_count += pichu_count(board,board[row][col], row, col)
            elif board[row][col] == 'W':
                white_count += pikachu_count(board,board[row][col], row, col) 
            elif board[row][col] == 'B':
                black_count += pikachu_count(board,board[row][col], row, col)
            elif board[row][col] == '@':
                white_count += raichu_count(board,board[row][col], row, col)
            elif board[row][col] == '$':
                black_count += raichu_count(board,board[row][col], row, col)
    
    return black_count, white_count
                       

def pichu_succ(board, pichu, row, col):
    newboard = copy.deepcopy(board)
    pichu_succ_list = []
    
    if pichu == 'b':
        jump_flag = False
        count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)): #top-left diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break
        

        jump_flag = False
        count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))): #top-right diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        return pichu_succ_list

            
    if pichu =='w':
        jump_flag = False
        count = 0
        k = 0
        m = 0
        for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)): #bottom-left diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
        
            
        jump_flag = False
        count = 0
        k = 0
        m = 0
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))): #bottom-right
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break

        return  pichu_succ_list        
                

def pikachu_succ(board, pikachu, row, col):
    top = 0
    bottom = 0
    left = 0
    right = 0

    pikachu_succ_list = []
    newboard = copy.deepcopy(board)

    jump_flag = False
    count = 0

    if pikachu == 'B':
        jump_flag = False
        count = 0
        k = 10000
        opp_i = 1000
        opp_j = 1000
        for i in range(row-1,-1,-1): # top direction
            k=i
            if (jump_flag == False and count==2):
                # print("jf =false count=2")
                break
            if (jump_flag == True and  count ==3):
                # print("jf= true count=3 or top = 2")
                break

            if (jump_flag == True and top ==0 and count ==2): # count = 2 is correct
                # print("jf=true top = 0 and cpunt = 2")
                break

            if (board[i][col] == '.' and jump_flag == False):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                if (k==0 and newboard[k][col] == 'B'):
                    newboard[k][col] = '$'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                top += 1
                count +=1
                # print(row," ",col," goes up: at ",i," ",col)
            elif (board[i][col] == '.' and jump_flag == True):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[opp_i][opp_j] = '.'
                if (k==0 and newboard[k][col] == 'B'):
                    newboard[k][col] = '$'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                if top == 0:
                    top += 2
                elif top == 2:
                    top +=1 
                count +=1
                # print(row," ",col," takes a jump at ",i," ",col)
            elif (board[i][col] in 'wW'):
                if jump_flag == False: 
                    jump_flag = True
                    # print(row," ",col," at same position as opponent, ready to jump at ",i," ",col)
                opp_i = i
                opp_j = col
                count += 1
            elif (board[i][col] in 'B@$'):
                # print(row," ",col," at same position as teammate, break the loop",i," ",col)
                break
        
        

    if pikachu == 'W':
        jump_flag = False
        count = 0
        k=0
        opp_i = 1000
        opp_j = 1000
        for i in range(row+1,len(board)): # bottom direction
            k=i
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and  count ==3):
                break
            if (jump_flag == True and bottom ==0 and count ==2):
                break
            

            if (board[i][col] == '.' and jump_flag == False):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                if (k==len(board)-1 and newboard[k][col] == 'W'):
                    newboard[k][col] = '@'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                bottom +=1
                count +=1
                # print(row," ",col," goes down: at ",i," ",col)
            elif (board[i][col] == '.' and jump_flag == True):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[opp_i][opp_j] = '.'
                if (k==len(board)-1 and newboard[k][col] == 'W'):
                    newboard[k][col] = '@'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                if bottom == 0:
                    bottom += 2
                elif bottom == 2:
                    bottom +=1 
                count +=1
                # print(row," ",col," takes a jump at ",i," ",col)
            elif (board[i][col] in 'bB'):
                if jump_flag == False: 
                    jump_flag = True
                    # print(row," ",col," at same position as opponent, ready to jump at ",i," ",col)
                opp_i = i
                opp_j = col
                count += 1
            elif (board[i][col] in 'W@$'):
                # print(row," ",col," at same position as teammate, break the loop",i," ",col)
                break
        
    

    jump_flag = False
    count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(col-1,-1,-1): # left direction
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and count ==3):
            break
        if (jump_flag == True and left ==0 and count ==2):
                break

        if (board[row][i] == '.' and jump_flag == False):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i+1] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            left +=1
            count +=1
            # print(row," ",col," goes left: at ",row," ",i)
        elif (board[row][i] == '.' and jump_flag == True):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[opp_i][opp_j] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            if left == 0:
                left += 2
            elif left == 2:
                left +=1 
            count +=1
            # print(row," ",col," takes a jump at ",row," ",i)
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag = True
                # print(row," ",col," at same position as opponent, ready to jump at ",row," ",i)
            opp_i = row
            opp_j = i
            count += 1
        elif (pikachu =='W' and board[row][i] in 'W@$') or (pikachu =='B' and board[row][i] in 'B@$'):
                # print(row," ",col," at same position as teammate, break the loop",row," ",i)
                break

    jump_flag = False
    count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(col+1,len(board[0])): # right direction
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and count ==3): 
            break
        if (jump_flag == True and right ==0 and count ==2):
                break

        if (board[row][i] == '.' and jump_flag == False):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i-1] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            right +=1
            count +=1
            # print(row," ",col," goes right: at ",row," ",i)
        elif (board[row][i] == '.' and jump_flag == True):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[opp_i][opp_j] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            if right == 0:
                right += 2
            elif right == 2:
                right +=1 
            count +=1
            # print(row," ",col," takes a jump at ",row," ",i)
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag = True
                # print(row," ",col," at same position as opponent, ready to jump at ",row," ",i)
            opp_i = row
            opp_j = i
            count += 1
        elif (pikachu =='W' and board[row][i] in 'W@$') or (pikachu =='B' and board[row][i] in 'B@$'):
                # print(row," ",col," at same position as teammate, break the loop",row," ",i)
                break
    
    return pikachu_succ_list
            

def raichu_succ(board, raichu, row, col):
    
    raichu_succ_list = []
    newboard = copy.deepcopy(board)

    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(row-1,-1,-1): # top direction
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = col
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(row+1,len(board)): # bottom direction
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = col
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(col-1,-1,-1): # left direction
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = row
                opp_j = i
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[row][i] in '@wW') or (raichu == '$' and board[row][i] in '$bB')):
            break

        
    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(col+1,len(board[0])): # right direction
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = row
                opp_j = i
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[row][i] in '@wW') or (raichu == '$' and board[row][i] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)): # top-left diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = j
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))): # top-right diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = j
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)): # bottom-left diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = j
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))): # nottom-right diagonal
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag = True
                opp_i = i
                opp_j = j
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    return raichu_succ_list


def succ(board, player):
    all_successor = []

    if player == 'w':
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 'w' :
                    all_successor += pichu_succ(board,board[row][col], row, col)
                elif board[row][col] in 'W':
                    all_successor += pikachu_succ(board,board[row][col], row, col)
                elif board[row][col] in '@':
                    all_successor += raichu_succ(board,board[row][col], row, col)

    elif player == 'b':
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 'b' :
                    all_successor += pichu_succ(board,board[row][col], row, col)
                elif board[row][col] in 'B':
                    all_successor += pikachu_succ(board,board[row][col], row, col)
                elif board[row][col] in '$':
                    all_successor += raichu_succ(board,board[row][col], row, col)

    return all_successor
            


def es(board):
    h3_black, h3_white = heuristic3(board)
    return 2*heuristic1(board) + 5*heuristic2(board) - 4*(h3_black - h3_white)
    # return heuristic1(board) + heuristic2(board) 


def minimaxpruning(board,player):

        hcount = 0
        evalues = []
        alpha = -(10^5)
        beta = 10^5
        if player =='w':
            # print("=========================== w successor ====================")
            for i in succ(board, 'w'):
                hcount=0
                evalues.append(min_val(i,alpha,beta,hcount))
                # for row in i:
                #     print(*row)
                # print(evalues[-1])
            # print("heuristic values:",evalues)
            return succ(board, player)[evalues.index(max(evalues))],max(evalues)
        elif player =='b':
            # print("=========================== b successor ====================")
            for i in succ(board, 'b'):
                hcount=0
                evalues.append(max_val(i,alpha,beta,hcount))
                # for row in i:
                #     print(*row)
                # print(evalues[-1])
            # print("heuristic values:",evalues)
            return succ(board, player)[evalues.index(min(evalues))] ,min(evalues)


def min_val(suc,alpha,beta,hcount):
        if hcount==4:
            return es(suc)
        else:
            # for row in suc:
            #     print(*row)
            # print("")
            for i in succ(suc, 'b'):
                beta = min(beta,max_val(i,alpha,beta,hcount+1))
                if alpha>=beta:
                    return beta
            return beta

def max_val(suc,alpha,beta,hcount):
        if hcount==4:
            return es(suc)
        else:
            # for row in suc:
            #     print(*row)
            # print("")
            for i in succ(suc, 'w'):
                alpha = max(alpha,min_val(i,alpha,beta,hcount+1))
                if alpha>=beta:
                    return alpha
            return alpha


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #

    # while timelimit:
    #     time.sleep(1)
    #     yield minimaxpruning(board,player)
    #     timelimit -= 1

    # height = 3
    # while True:
        # print("solution for height: ", height)
    return (minimaxpruning(board,player))
        # height += 1

     


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")


    # print successors at level 1
    demoSucc = string_to_board(board,N)
    # print("\n==============successors at level : 1================\n")
    # list_of_succ = succ(demoSucc, player)
    # boardcount = 0
    # for board1 in list_of_succ:
    #     for row in board1:
    #         print(*row)
    #     print("")
    #     boardcount += 1
    # print("total successors at level 1: ", boardcount)


    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    newboard = string_to_board(board,N)


    board,heuristic = find_best_move(newboard, N, player, timelimit)
    boardlist = [y for x in board for y in x]
    print(boardlist)
    print("".join(boardlist))
    for row in board:
        print(*row)
    
    print("Heuristic: ", heuristic)
        # print("")
    # print(board) # actual output

    # string_to_board(board, N)


    
        