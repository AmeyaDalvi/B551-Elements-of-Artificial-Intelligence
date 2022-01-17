#!/usr/local/bin/python3
#
# Authors:
# Ameya Dalvi [abdalvi]
# Henish Shah [henishah]
# Shubham Bhagat [snbhagat]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from typing import final
from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np
import copy

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)



# return a column as an array
def column(matrix, i):
    return [row[i] for row in matrix]




#----------------------------------edge detection using simple model-----------------------------------
def simple(image_array):
    airice_simple = []
    icerock_simple = []

    for i in range(len(image_array[0])):
        airice_arr = []
        icerock_arr = []

        airice_arr.append(column(image_array,i))
        icerock_arr.append(column(image_array,i))
        airice_index = airice_arr[0].index(min(airice_arr[0]))

        icerock_arr1 = icerock_arr[0][airice_index+10:]
        minicerock = min(icerock_arr1)
        icerock_index = icerock_arr[0].index(minicerock)

        # airice_prob = airice_index/(sum(airice_arr)/255)
        airice_simple.append(airice_index)

        # icerock_prob = icerock_index/(sum(icerock_arr)/255)
        icerock_simple.append(icerock_index)

        airice_arr.clear()
        icerock_arr.clear()
        icerock_arr1.clear()
    
    return airice_simple, icerock_simple




# ----------------------------------edge detection using viterbi------------------------------------------

# calculate transition probability
def trans_prob(image_array, row, col, prob_hmm):
    transition_probab=[]
    for i in range(image_array.shape[0]):
        if abs(i-row)> 10 and i!=row:        # if pixel belogs to different row but within thw 10 pirxel threshold
            trans = -np.log(0.1)
        elif abs(i-row)<10 and i!=row:
            trans = -np.log((1/abs(i-row)))
        else:
            trans = -np.log(0.1)
        transition_probab.append(prob_hmm[(i,col-1)][0]+trans)
    return transition_probab


#  calculte emission probability
def emiss_prob(image_array, row, col):
    if row<int(image_array.shape[0]):
        return (image_array[row,col]/sum(image_array[:,col]))
    else:
        return (image_array[row,col]/sum(image_array[:,col]))*image_array.shape[0]


def emiss_prob_feedback(image_array, row, col):
    return (image_array[row,col]/sum(image_array[:,col]))*image_array.shape[0]


# viterbi for airice boundary
def viterbi(image_array, init):
    prob_hmm = {}
    
    # init = [-np.log(1/image_array.shape[0])]*image_array.shape[0]

    # initial probability for the t=0 is initial * emission
    for row in range(0, image_array.shape[0]):
        prob_hmm[(row,0)] = (init[row]*emiss_prob(image_array,row,0),"")
    
    for col in range(1, image_array.shape[1]):
        for row in range(0, image_array.shape[0]):
            trans = trans_prob(image_array, row, col, prob_hmm) # get transition probability from col-1 to col
            emiss = emiss_prob(image_array, row, col) # get emission probability of col

            trans_index = trans.index(min(trans))       #index of min element for pixel
            
            pixel_prob = np.min(trans) + emiss # probability of pixel at row,col

            pixel_path = prob_hmm[(trans.index(min(trans)), col-1)][1]+ " " + str(trans_index) # path to reach pixel at row,col
            prob_hmm[(row,col)] = (pixel_prob,pixel_path) # put probability and path in dictionary
        
    last_col = [prob_hmm[(i,image_array.shape[1]-1)][0] for i in range(image_array.shape[0])] # get last col of image
    last_col_index = last_col.index(min(last_col)) # get index minimum most pixel

    edge_path = prob_hmm[(last_col_index,image_array.shape[1]-1)][1] # get path of edge from start to end pixel (last_col_index)
    edge_path = edge_path[1:]

    edge_hmm = edge_path.split(" ")
    edge_hmm=[int(i) for i in edge_hmm] # final boundary as index values
    edge_hmm.append(last_col_index)
    # print("The length of edge_hmm: ",len(edge_hmm))
    return edge_hmm



def viterbi_feedback(image_array, init):
    prob_hmm = {}
    
    # init = [-np.log(1/image_array.shape[0])]*image_array.shape[0]

    # initial probability for the t=0 is initial * emission
    for row in range(0, image_array.shape[0]):
        prob_hmm[(row,0)] = (init[row]*emiss_prob_feedback(image_array,row,0),"")
    
    for col in range(1, image_array.shape[1]):
        for row in range(0, image_array.shape[0]):
            trans = trans_prob(image_array, row, col, prob_hmm) # get transition probability from col-1 to col
            emiss = emiss_prob_feedback(image_array, row, col) # get emission probability of col

            trans_index = trans.index(min(trans))       #index of min element for pixel
            
            pixel_prob = np.min(trans) + emiss # probability of pixel at row,col

            pixel_path = prob_hmm[(trans.index(min(trans)), col-1)][1]+ " " + str(trans_index) # path to reach pixel at row,col
            prob_hmm[(row,col)] = (pixel_prob,pixel_path) # put probability and path in dictionary
        
    last_col = [prob_hmm[(i,image_array.shape[1]-1)][0] for i in range(image_array.shape[0])] # get last col of image
    last_col_index = last_col.index(min(last_col)) # get index minimum most pixel

    edge_path = prob_hmm[(last_col_index,image_array.shape[1]-1)][1] # get path of edge from start to end pixel (last_col_index)
    edge_path = edge_path[1:]

    edge_hmm = edge_path.split(" ")
    edge_hmm=[int(i) for i in edge_hmm] # final boundary as index values
    edge_hmm.append(last_col_index)
    # print("The length of edge_hmm: ",len(edge_hmm))
    return edge_hmm







# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ] # get col, row for airice
    gt_icerock = [ int(i) for i in sys.argv[4:6] ] # col, row for icerock

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.



    # ----------------- using Simple model ------------------------------------


    airice_simple, icerock_simple = simple(image_array) 


    # ------------------ using viterbi (HMM) ----------------------------------


    # initial probability for Q0 (first pixel column)
    init = [-np.log(1/image_array.shape[0])]*image_array.shape[0]

    # get airice boundary using viterbi model
    # print("airice viterbi")
    airice_hmm= viterbi(image_array, init)
    airice_inter = copy.deepcopy(airice_hmm)

    # create white pixel margin for icerock boundary
    input_image1 = copy.deepcopy(input_image)
    for i in range(-5,10):
        airice_inter = [x + i for x in airice_hmm]
        new_image1 = draw_boundary(input_image1, airice_inter, (255, 255, 255), 2) # new image with white margin
        airice_inter.clear()

    # imageio.imwrite("white_output.png", new_image1)
    

    #  get new image array with white margin
    image_array1 = array(new_image1.convert('L'))

    #get icerock boundary using viterbi
    # print("icerock hmm")
    icerock_hmm = viterbi(image_array1, init)


    # ------------------------------ for human feedback -----------------------------

    # split imag based on coordinates
    image_array_1 = image_array[:,0:gt_airice[0]]
    image_array_2 = image_array[:,gt_airice[0]:image_array.shape[1]]

    
    # temp images after split
    temp_image1 = Image.fromarray(image_array_1)
    temp_image2 = Image.fromarray(image_array_2)

    new_init_1 = np.ones(image_array.shape[0])

    #handling the column error
    if gt_airice[0]!=0:
        image_array_1=np.flip(image_array_1, 1) # flip image
        # print("airice feedback part 1")
        airice_path_1 = viterbi(image_array_1, new_init_1)
        airice_path_1 = airice_path_1[::-1]
    # print("airice feedback part 2")
    airice_path_2 = viterbi(image_array_2, new_init_1)

    airice_feedback = airice_path_1[:-1] + airice_path_2 # get path for airice


    # imageio.imwrite("white_output_2.png", new_image1)

    #  split image based on cordinates
    image_array2 = array(new_image1.convert('L'))
    image_array_3 = image_array2[:,0:gt_icerock[0]]
    image_array_4 = image_array2[:,gt_icerock[0]:image_array.shape[1]]

    new_init_2 = np.ones(image_array.shape[0])

    if gt_icerock[0]!=0:
        image_array_3=np.flip(image_array_3, 1) # flip image
        # print("icerock feedback part 1")
        icerock_path_1 = viterbi_feedback(image_array_3, new_init_2)
        icerock_path_1 = icerock_path_1[::-1]
    # print("icerock feedback part 2")
    icerock_path_2 = viterbi_feedback(image_array_4, new_init_2)

    icerock_feedback = icerock_path_1[:-1] + icerock_path_2 # get pathfor icerock



    # airice_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    # airice_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    # airice_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    # icerock_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    # icerock_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    # icerock_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)

    
    # output of temp (split image)
    # imageio.imwrite("air_ice_output.png", temp_image1)
    # imageio.imwrite("ice_rock_output.png", temp_image2)
    
    
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
