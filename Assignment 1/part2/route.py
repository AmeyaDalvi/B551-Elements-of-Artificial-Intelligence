#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Henish Shah (2000845343)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
# !/usr/bin/env python3
import sys
from math import tanh
from math import dist
import math
import pdb

# This functions returns a dictionary with a particular city as key and all the nodes it is connected to as its values

def parse_map_edit1(filename):
    d1 = {}
    with open(filename, "r") as f:
        #print(len(f.read()('\n').split(" ")))
         for line in f.read().split('\n'):
            temp = line.split(' ')
            if len(temp)<2: # A list with less than 2 elements means it is of no use to us and thus, we discard it. 
                continue

            if temp[0] in d1.keys():
                d1[temp[0]][temp[1]]={'distance':int(temp[2]),'speed':int(temp[3]),'highway':temp[4]}
                if temp[1] in d1.keys():
                    d1[temp[1]][temp[0]]={'distance':int(temp[2]),'speed':int(temp[3]),'highway':temp[4]}
                else:
                    d1[temp[1]]={temp[0]:{'distance':int(temp[2]),'speed':int(temp[3]),'highway':temp[4]}}

            else:
            #    d1[temp[0]]=[temp[1:]]
                d1[temp[0]]={temp[1]:{'distance':int(temp[2]),'speed':int(temp[3]),'highway':temp[4]}}
                d1[temp[1]]={temp[0]:{'distance':int(temp[2]),'speed':int(temp[3]),'highway':temp[4]}}
    return d1

dict1_edit1 = parse_map_edit1('road-segments.txt')

def parse_map_2(filename):
    d2 = {}
    with open(filename, "r") as f:
            #print(len(f.read()('\n').split(" ")))
            for line in f.read().split('\n'):
                temp = line.split(' ')
                if len(temp)<2: # A list with less than 2 elements means it is of no use to us and thus, we discard it. 
                    continue
                d2[temp[0]]=[float(temp[1]),float(temp[2])]
            return d2

dict2 = parse_map_2('city-gps.txt')


'''Formula for haversine distance referenced from
http://www.codecodex.com/wiki/Calculate_Distance_Between_Two_Points_on_a_Globe#Python
'''
def haversine(lon1,lat1,lon2,lat2):
    d_latt=lat2-lat1
    d_long=lon2-lon1
    a = math.sin(d_latt/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_long/2)**2
    c = 2 * math.asin(math.sqrt(a))
    ans = 3958.756 * c
    return ans


def heuristic(city,end_city):
    #pdb.set_trace()
    if city in dict2.keys():
        ans = haversine(dict2[end_city][0],dict2[end_city][1],dict2[city][0],dict2[city][1])
    else:
        ans=0
    return ans


def segments(start,previous_city,city,end_city):
    main_list = ()
    for i in dict1_edit1[previous_city].items():
        if i[0]==city:
            main_list = ((i[0],(i[1]['distance']/i[1]['speed']),i[1]['distance']),(heuristic(city,end_city)/haversine(dict2[start][0],dict2[start][1],dict2[end_city][0],dict2[end_city][1]))+1)
            break
    return main_list


def distance(start,previous_city,city,end_city):
    temp_dist=1000000
    main_list = ()
    for i in dict1_edit1[previous_city].items():
        if i[0]==city:
            main_list = ((i[0],(i[1]['distance']/i[1]['speed'],i[1]['distance'])),30*(heuristic(city,end_city)/haversine(dict2[start][0],dict2[start][1],dict2[end_city][0],dict2[end_city][1]))+i[1]['distance'])
            break
    return main_list


def time(start,previous_city,city,end_city):
    for i in dict1_edit1[previous_city].items():
        if i[0]==city:
            main_list = ((i[0],(i[1]['distance']/i[1]['speed']),i[1]['distance']),40*(heuristic(city,end_city)/haversine(dict2[start][0],dict2[start][1],dict2[end_city][0],dict2[end_city][1]))+(i[1]['distance']/i[1]['speed']))
    return main_list


def delivery(start,previous_city,city,end_city,t_trip):
    final_time=0
    for i in dict1_edit1[previous_city].items():
        if i[0]==city:
            if i[1]['speed']>=50:
                final_time=(i[1]['distance']/i[1]['speed'])+ 2*tanh(i[1]['distance']/1000)*((i[1]['distance']/i[1]['speed'])+t_trip)
                main_list = ((i[0],final_time,i[1]['distance']),40*(heuristic(city,end_city)/haversine(dict2[start][0],dict2[start][1],dict2[end_city][0],dict2[end_city][1]))+final_time)
            
            else:
                final_time = i[1]['distance']/i[1]['speed']
                main_list = ((i[0],final_time,i[1]['distance']),40*(heuristic(city,end_city)/haversine(dict2[start][0],dict2[start][1],dict2[end_city][0],dict2[end_city][1]))+final_time)
    return main_list


def cost_fn(cost,start,c_node,succ,end,t_trip):

    if cost=='distance':
        a = distance(start,c_node,succ,end)
    elif cost=='segments':
        a = segments(start,c_node,succ,end)
    elif cost=='time':
        a = time(start,c_node,succ,end)
    elif cost=='delivery':
        a = delivery(start,c_node,succ,end,t_trip)
    return a


def successors(city):
    return [i for i in dict1_edit1[city].keys()]


def get_route(start, end, cost):

    fringe = [((start,0,0),0)] # Initialising the fringe with ((start_city,time,distance),h(s)+g(s))
    paths = [[(start,0,0,'',0)]]
    visited_node = [start]

    while fringe:
        fringe=sorted(fringe,key=lambda x:x[1])
        c_node = fringe.pop(0)

        for succ in successors(c_node[0][0]):
            #pdb.set_trace()
            if succ == end:
                count=1
                for i in paths:
                        
                        for j in i: 
                            if c_node[0][0] in i[i.index(j)] and i.index(j)==len(i)-1:
                                for k in dict1_edit1[c_node[0][0]].keys():
                                    if k==succ:
                                        paths[paths.index(i)].append((succ,dict1_edit1[c_node[0][0]][k]['distance']/dict1_edit1[c_node[0][0]][k]['speed'],dict1_edit1[c_node[0][0]][k]['distance'],dict1_edit1[c_node[0][0]][k]['highway'],dict1_edit1[c_node[0][0]][k]['speed']))
                                temp_paths=paths
                                ans_path=i
                                count=0
                                break
                            
                            elif c_node[0][0] in i[i.index(j)] and i.index(j)!=len(i)-1:
                                l = i[:i.index(j)+1]
                                for k in dict1_edit1[c_node[0][0]].keys():
                                    if k==succ:
                                        l.append((succ,dict1_edit1[c_node[0][0]][k]['distance']/dict1_edit1[c_node[0][0]][k]['speed'],dict1_edit1[c_node[0][0]][k]['distance'],dict1_edit1[c_node[0][0]][k]['highway'],dict1_edit1[c_node[0][0]][k]['speed']))
                                temp_paths = paths
                                temp_paths.append(l)
                                ans_path=l
                                count=0
                                break
                        if count==0:
                            break
                
                paths=temp_paths
                total_time=0
                total_dist=0.0
                route_taken=[]
                delivery_time=0

                t_trip=0
                for i in range(len(ans_path)):
                    #pdb.set_trace()
                    if i!=0:
                        delivery_time += delivery(start,ans_path[i-1][0],ans_path[i][0],end,t_trip)[0][1]
                    t_trip+=ans_path[i][1]

                for i in range(len(ans_path)):
                    total_time+=ans_path[i][1]
                    total_dist+=ans_path[i][2]
                    if i!=0:
                        route_taken.append((f'{ans_path[i][0]}',f'{ans_path[i][3]} for {ans_path[i][2]} miles'))
                

                return {"total-segments" : len(route_taken), 
                        "total-miles" : total_dist, 
                        "total-hours" : total_time, 
                        "total-delivery-hours" : delivery_time, 
                        "route-taken" : route_taken}

            else:

                if succ not in visited_node:

                    count=1

                    for i in paths:
                        for j in i: 
                            
                            if c_node[0][0] in i[i.index(j)] and i.index(j)==len(i)-1:
                                for k in dict1_edit1[c_node[0][0]].keys():
                                    if k==succ:
                                        paths[paths.index(i)].append((succ,dict1_edit1[c_node[0][0]][k]['distance']/dict1_edit1[c_node[0][0]][k]['speed'],dict1_edit1[c_node[0][0]][k]['distance'],dict1_edit1[c_node[0][0]][k]['highway'],dict1_edit1[c_node[0][0]][k]['speed']))
                                temp_paths=paths
                                t_trip_path=i
                                t_trip=0
                                for i in t_trip_path[:-1]:
                                    t_trip+=i[1]

                                hsgs=0
                                for y in range(1,len(t_trip_path)):
                                    #pdb.set_trace()
                                    r = t_trip_path[y][0]
                                    s = t_trip_path[y-1][0]
                                    infos,hs = cost_fn(cost,start,s,r,end,t_trip)
                                    hsgs+=hs
                                infos1,hs1=cost_fn(cost,start,c_node[0][0],succ,end,t_trip)
                                fringe.append((infos1,hsgs))
                                
                                count=0
                                break
                            elif c_node[0][0] in i[i.index(j)] and i.index(j)!=len(i)-1:
                                l = i[:i.index(j)+1]

                                for k in dict1_edit1[c_node[0][0]].keys():
                                    if k==succ:
                                        l.append((succ,dict1_edit1[c_node[0][0]][k]['distance']/dict1_edit1[c_node[0][0]][k]['speed'],dict1_edit1[c_node[0][0]][k]['distance'],dict1_edit1[c_node[0][0]][k]['highway'],dict1_edit1[c_node[0][0]][k]['speed']))
                                temp_paths = paths
                                temp_paths.append(l)
                                t_trip_path=l
                                t_trip=0
                                for i in t_trip_path[:-1]:
                                    t_trip+=i[1]
                                hsgs=0
                                for i in range(1,len(l)):
                                    r = l[i][0]
                                    s = l[i-1][0]
                                    infos,hs = cost_fn(cost,start,s,r,end,t_trip)
                                    hsgs+=hs
                                infos1,hs1=cost_fn(cost,start,c_node[0][0],succ,end,t_trip)
                                fringe.append((infos1,hsgs))

                                count=0
                                break
                        if count==0:
                            break            
                    paths=temp_paths
                else:
                    continue
                
                visited_node.append(succ)            

"""
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # Parse the map from a given filename


    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    # return {"total-segments" : len(route_taken), 
    #         "total-miles" : 51., 
    #         "total-hours" : 1.07949, 
    #         "total-delivery-hours" : 1.1364, 
    #         "route-taken" : route_taken}


#Please don't modify anything below this line

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


