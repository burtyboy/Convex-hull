"""
   Convex Hull Assignment: COSC262 (2017)
   Student Name: Josh Burt      
   Usercode: jbu71
"""

def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    raw_points = open(filename)
    
    listPts = []
    for i in range(0, N):
        str_pt = raw_points.readline()
        (pta,ptb) = str_pt.split()
        listPts.append((float(pta),float(ptb)))
        
    return listPts


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of 'h' tuples
          [(u0,v0), (u1,v1), ...]    
    """
    
    y_min_index = get_start_point(listPts)
    chull = []
    i  = 0
    v = 0
    k = y_min_index
    listPts.append(listPts[y_min_index])
    endpoint = listPts[i] #intialise endpoint so the program will run
    final_point = listPts[-1]
    while endpoint != final_point:
        chull.append(listPts[k])
        listPts[i], listPts[k] = listPts[k], listPts[i]
        j = i+1
        min_angle = 361
        for index in range(j, len(listPts)):
            angle = theta(listPts[i], listPts[index])
            if angle <= min_angle and angle >= v and listPts[index] != listPts[i]:
                min_angle = angle
                k = index
        if min_angle == v:
            chull.pop()  # removes any colinear points
        
        i+=1
        v = min_angle
        endpoint = listPts[k]
       
    return chull


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  
    """
    y_min_index = get_start_point(listPts)
    for i in range(0,len(listPts)):
        if i != y_min_index:
            angle = theta(listPts[y_min_index], listPts[i])
            listPts[i] = (listPts[i][0], listPts[i][1], angle)
        else:
            listPts[i] = (listPts[i][0], listPts[i][1], 0)
            
    
    listPts.sort(key = lambda item: item[2]) #sorts by the angle given in the [2] index of a tuple
    chull = [(listPts[0][0],listPts[0][1]), (listPts[1][0],listPts[1][1]), (listPts[2][0],listPts[2][1])]
    for j in range(3, len(listPts)):
        while not isCCW(chull[-2],chull[-1],listPts[j]):
            chull.pop()
        if line_fn(chull[-2],chull[-1],listPts[j]) == 0:
            print("colinear")
            chull.pop(-2) #removes a colinear point from the middle of the index
        chull.append((listPts[j][0], listPts[j][1]))
    
    return  chull


def amethod(listPts):
    """Returns the convex hull vertices computed using 
          a third algorithm
    """
    #Your implementation goes here    
    return chull


def get_start_point(listPts):
    """ Takes a list and returns the index of the point with the lowest y value
        if two points have equal y values it takes the "right-most" point of these two.
        """
    
    y_min_index = 0 #set to first point arbitrally
    for current_point_index in range(1, len(listPts)-1):
        point = listPts[current_point_index]
        if point[1] == listPts[y_min_index][1]:
            if point[0] > listPts[y_min_index][0]:
                y_min_index = current_point_index
        elif point[1] < listPts[y_min_index][1]:
            y_min_index = current_point_index
    return y_min_index


def theta(pointA, pointB):
    """ Implmentation of the Theta function as shown in lectures.
        using an aproximation to the angle to avoid Trigonometric functions
    """
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))
        
    if dx < 0:
        t = 2-t
    elif dy < 0:
        t = 4 + t
    
    return t*90
    
def line_fn(pointA, pointB, pointC):
    """ returns the gradient differance of 3 points is 0 if colinear"""
    return ((pointB[0] - pointA[0])*(pointC[1] - pointA[1]) - 
                (pointB[1] - pointA[1]) * (pointC[0] - pointA[0]))


def isCCW(pointA, pointB, pointC):
    """ Takes 3 points and calculates if the angle between them is a counter-clockwise turn,
        Returns True is it is
        """
    return line_fn(pointA, pointB, pointC) > 0
    
    
def main():
    listPts = readDataPts('Set_B.dat', 30000)  #File name, numPts given as example only
    giftwrap_run = (giftwrap(listPts))
    listPts = readDataPts('Set_B.dat', 30000) #You may replace these three print statements
    graham = (grahamscan(listPts))   #with any code for validating your outputs
    if len(giftwrap_run) == len(graham):
        print("Both are of equal Length: {}".format(len(giftwrap_run)))
        for i in range(0, len(giftwrap_run)):
            if giftwrap_run[i] != graham[i]:
                print("the lists differ at index {}, giftwrap: {} Grahams: {}".format(i, giftwrap_run[i], graham[i]))
        else:
            print("The lists are identical")
    else:
        print("The lists have differant lengths, giftwrap: {} Grahams: {}".format(len(giftwrap_run), len(graham)))
    #print (amethod(listPts))     

 
if __name__  ==  "__main__":
    main()