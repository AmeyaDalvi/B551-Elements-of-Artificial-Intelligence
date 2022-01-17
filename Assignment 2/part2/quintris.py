# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys


class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:

    def __init__(self):
        pass

    def down(self,state, score, piece,row,col):
        while not quintris.check_collision( state, score,piece, row+1, col):
            row += 1
        return (row,col)

    def transform(self,piece):
        plus  = [ " x ", "xxx", " x "]
        all_piece = []
        if piece == plus:
            all_piece.append((piece,''))
        else:      
            all_piece.append((piece,''))

            rot = quintris.rotate_piece(piece,90)
            all_piece.append((rot,'n'))

            b = quintris.rotate_piece(rot,90)
            all_piece.append((b,'nn'))

            c = quintris.rotate_piece(b,90)
            all_piece.append((c,'nnn'))

            d = quintris.hflip_piece(piece)
            all_piece.append((d,'h'))

            e = quintris.hflip_piece(rot)
            all_piece.append((e,'nh'))

            f = quintris.hflip_piece(b)
            all_piece.append((f,'hnn'))

            g = quintris.rotate_piece(d,90)
            all_piece.append((g,'hn'))

        return all_piece

    def left_right(self,best_suc,piece,row,col):

        best_suc_col = best_suc[0][1]
        lrstring = ''

        if best_suc_col - col > 0:
            lrstring = lrstring + 'm'*abs(best_suc_col - col)
        elif best_suc_col - col < 0:
            lrstring = lrstring + 'b'*abs(best_suc_col - col)
        else:
            lrstring = ''
        
        return lrstring

    #The idea for the heuristic functions mentioned below i.e Aggregate height, Complete Lines, Holes, Bumpiness is referenced from:
    #https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/ 
    def agg_height(self,board):
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

    def comp_lines(self,board):
        line_count=0
        for row in range(len(board)-1,-1,-1):
            if board[row].count('x') == len(board[row]):
                line_count+=1
            else:
                continue
        return line_count

    def holes(self,board):
        final_holes=0
        for col in range(len(board[0])):
            holes = 0
            count = 0
            for row in range(len(board)-1, -1, -1):
                if board[row][col] == ' ':
                        count +=1
                elif board[row][col] == 'x' and count !=0:
                        holes += count
                        count = 0    
            final_holes += holes
        return final_holes


    def bumpiness(self,board):
        bump=0
        for col in range(len(board[0])):
            height1=0
            height2=0
            count=0
            holes=0
            for row in range(len(board)-1,-1,-1):
                if col < len(board[0])-1:
                    if board[row][col] == ' ':
                        count +=1
                    elif board[row][col] == 'x' and count !=0:
                        height1 += count
                        count = 0                   
                    elif board[row][col] == 'x':
                        height1+=1

                    if board[row][col+1] == ' ':
                        count +=1
                    elif board[row][col+1] == 'x' and count !=0:
                        height1 += count
                        count = 0                   
                    elif board[row][col+1] == 'x':
                        height1+=1
                
            bump += abs(height1-height2)
        return bump

    #This is an extra heuristic that we have added which tries to maximis the number of x's row wise
    def line_fill(self,board):
        xcount=0
        for row in range(len(board)-1,-1,-1):
            xcount += int(board[row].count('x')**(3/2))
        return xcount
            

    def heuristic(self,state):
        return 200*self.comp_lines(state)+10*(self.line_fill(state))-25*(self.holes(state))-30*(self.agg_height(state))-5*(self.bumpiness(state))

    def succ(self, state,piece,transformation):
        suc = {}
        max_piece_length =0

        for i in range(len(state[0])-len(piece[0])+1): 
            score = self.comp_lines(state)
            r,c= self.down(state,score,piece,0,i) 
            temp_suc = quintris.place_piece(state,score,piece,r,c)
            key = tuple(temp_suc[0],)
            suc[key]=[(r,c),transformation,self.heuristic(temp_suc[0])]
        return suc


    def all_succ(self, state, piece):
        final_succ_list = {}
        for p,t in self.transform(piece):
            temp_suc_dict = self.succ(state,p,t)
            for k in temp_suc_dict.keys():
                final_succ_list[k] = temp_suc_dict[k]
        return final_succ_list


    def best_succ(self,all_succ_dict):
        max_heuristic = -100000
        for i in all_succ_dict.items():
            if i[1][2]>max_heuristic:
                max_heuristic=i[1][2]
                best_suc = i 
        return best_suc 


    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    def get_moves(self, quintris):
        # print("inside get moves")
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        final_str = ''
        count=0
        main_succ2 = {}
        board = quintris.get_board()
        piece,row,col = quintris.get_piece()
        test_suc = self.all_succ(board, piece)
        # print(quintris.get_next_piece())
        # print("test_succ", test_suc)
        for i in test_suc.keys():
            temp_succ2 = self.all_succ(list(i), quintris.get_next_piece())
            for j in temp_succ2.keys():
                temp_succ2[j].append(i) 
                if count > 0:
                    main_succ2.update(temp_succ2)
                else:
                    main_succ2 = temp_succ2
                count+=1
        

        best_suc2 = self.best_succ(main_succ2)
        best_suc = test_suc[best_suc2[1][3]]
        lrstring = self.left_right(best_suc, piece, row, col)
        if best_suc[0][1] - col > 0:
            final_str = best_suc[1] + lrstring
        elif best_suc[0][1] - col < 0:
            final_str = lrstring + best_suc[1]
        else:
            final_str = ''
        print(final_str)
        return final_str
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        final_str = ''
        count=0
        main_succ2 = {}
        board = quintris.get_board()
        piece,row,col = quintris.get_piece()
        test_suc = self.all_succ(board, piece)
        # print(quintris.get_next_piece())
        # print("test_succ", test_suc)
        for i in test_suc.keys():
            temp_succ2 = self.all_succ(list(i), quintris.get_next_piece())
            for j in temp_succ2.keys():
                temp_succ2[j].append(i) 
                if count > 0:
                    main_succ2.update(temp_succ2)
                else:
                    main_succ2 = temp_succ2
                count+=1
        

        best_suc2 = self.best_succ(main_succ2)
        best_suc = test_suc[best_suc2[1][3]]
        lrstring = self.left_right(best_suc, piece, row, col)
        if best_suc[0][1] - col > 0:
            final_str = best_suc[1] + lrstring
        elif best_suc[0][1] - col < 0:
            final_str = lrstring + best_suc[1]
        else:
            final_str = ''
        return final_str


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



