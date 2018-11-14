"""
this is the guide to help with orientattion
and find what's left and right is.
Lef and right is relative to the orientation,
so it's important to know which direction
we're moving. If you're moving north,
left is east. But if you're moving
south, left is west.

This little map is how the "tiny" maze
looks like.
        y

    ---X------
    -11111111-
    -1----1-1-
    -111-11-1-
    -1-1-1--1-
x   -11111-11-
    -----1----
    -1-1-1--1-
    -11111111-
    -------1--

        ^
        |
      north

<-- east  west -->

      south
        |
"""


from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000
import time


# I added these guys to make sure I don't get into
# an infinite loop if I make a mistake while I'm developing the code.
# it's usualy a good idea using "while" loops
MAXITER = 1000
CURRENTITER = 0

image = "tiny.png"
##image = "small.png"
##image = "normal.png"
##image = "braid200.png"
##image = "braid2k.png"
##image = "perfect15k.png"
#image = "p15ktest2.png"

output_file = "Out.png"
startPos = None
endPos = None

print("Loading Map Images")
t0 = time.time()
im = Image.open(image)
width, height = im.size[0], im.size[1]

# this is the list where your boss stores
# the pixel values of the image.
# 1 is white, 0 is black.
data = list(im.getdata(0))

listMap = []
rowList = []
rowCount = 0

# here he breakes down the pixel values into a
# two dimensional list, so we can check the pixel
# values as coordinates. The "listmap" variable
# looks like the image. listmap[0][0] is the
# top left corner pixe of the image
for i in data:
    rowCount = len(rowList)

    if rowCount < width:
        rowList.append(i)
    rowCount = len(rowList)

    if rowCount >= width:
        listMap.append(rowList)
        rowList = []

##for l in listMap:
##    print(l)

idx = 0


# here he just finds where the first and the last
# steps are. he scans the first and the last rows
# of the image, and if it's white, he assumes
# that's the start and the end position.
for i in listMap[0]:
    if i == 1:
        startPos = idx
        break
    idx += 1
#print(startPos)
idx = 0
for i in listMap[-1]:
    if i == 1:
        endPos = idx
        break
    idx += 1
#print(endPos)

if startPos is None or endPos is None:
    raise ValueError ("Start or End Could Not Be Found")
t1 = time.time()
total = t1 - t0
print("Time Taken To Load Image:" , total)

print("Starting Maze Solving")
t0 = time.time()
print("Start Time: ", t0)

"""
Use this space for helper functions and declaring varibales
"""

# I'm initializing some values. like the startPos
# and endPos are single integers. I turn them to coordinates
initcoord = (0, startPos)
endcoord = (height-1, endPos)

# I initialize where we start the maze
currentPos = initcoord

# and set the initial orientation to south.
orientation = 'south'

# add the first step coordinate to the solution list
resultpath = (initcoord,)
is_leftwall = None
is_frontwall = None


def check_left_wall(pos, orientation):
    """
    given the current coordinate we're at
    and the orientation this function
    checks if there's a wall to the left
    and returns true or false.

    this is the reason why we have to know
    where we're heading as the orientation.
    """
    if orientation == 'north':
        leftcoord = pos[0], pos[1]-1
    elif orientation == 'south':
        leftcoord = pos[0], pos[1]+1

    elif orientation == 'east':
        leftcoord = pos[0]+1, pos[1]
    elif orientation == 'west':
        leftcoord = pos[0]-1, pos[1]

    # the next part is an ugly one. if we're on the edge
    # of the maze checking if there's a wall to the left
    # will error, because the coordinate we're checking
    # is outside of the maze, so the coordinate doesn't
    # exist in the list, so we get an error. This should
    # be written much nicer, but this get's the job done.
    # if the coordinate errors when I check it, the code
    # assumes there's a wall
    try:
        result = not bool(listMap[leftcoord[0]][leftcoord[1]])
    except:
        result = True

    return result



def check_front_wall(pos, orientation):
    """
    this is the same as the left wall function.
    Just check different coordinates.
    """
    if orientation == 'north':
        frontcoord = pos[0]-1, pos[1]
    elif orientation == 'south':
        frontcoord = pos[0]+1, pos[1]
    elif orientation == 'east':
        frontcoord = pos[0], pos[1]-1
    elif orientation == 'west':
        frontcoord = pos[0], pos[1]+1

    try:
        result = not bool(listMap[frontcoord[0]][frontcoord[1]])
    except:
        result = True

    return result



def turn(orientation, clockwise=True):
    """
    this function turns. meaning it changes
    orientation. I only wrote it to turn in
    one direction. If the code needs to turn
    to the other side, it simple turns
    3 times. That makes it simple :)
    this simple sets our new orientation
    based on our current orientation
    and returns it
    """
    repeat = range(3) if clockwise else range(1)

    for turn in repeat:
        if orientation == 'north':
            orientation = 'west'
        elif orientation == 'west':
            orientation = 'south'
        elif orientation == 'south':
            orientation = 'east'
        elif orientation == 'east':
            orientation = 'north'

    return orientation




def move(pos, orientation):
    """
    given a position coordinate
    and our current orientation,
    this guy calculates a step forward
    and returne the new coordinate.

    this is the other reason we need to store and know
    our current orientation. Moving forward one step
    means different things if you're facing
    north and another thing when you're
    facing south.
    """
    # if pos[0] < height-1:
    #     newpos = pos[0]+1, pos[1]
    # else:
    #     newpos = pos[0], pos[1]+1
    if orientation == 'north':
        newpos = pos[0]-1, pos[1]
    elif orientation == 'west':
        newpos = pos[0], pos[1]+1
    elif orientation == 'south':
        newpos = pos[0]+1, pos[1]
    elif orientation == 'east':
        newpos = pos[0], pos[1]-1

    return newpos



# This is the main event loop where everything is happening.
# this is the part where the algorythm we found online
# is happening
while True:

    """
    Michael put your movement code here

    """
    # I start by checking the walls and store this info
    # so I can make the decisions later
    is_leftwall = check_left_wall(
        pos=currentPos, orientation=orientation)
    is_frontwall = check_front_wall(
        pos=currentPos, orientation=orientation)

    print('\n--> current pos:', currentPos)
    print('--> orientation:', orientation)
    print('--> is wall to left:', is_leftwall)
    print('--> is wall to front:', is_frontwall)

    # Dont for get to change this to something that sets completed to True

    # this part checks if the coordinate of our current
    # position is the end position. if it is, we found our way
    # out and can terminate the main event loop
    if currentPos == endcoord:
        break
        print("Found The Exit")


    # here I check if there's a wall to the left or not.
    if not is_leftwall:
        # if there's no wall then turn, move and store the coordinates
        orientation = turn(orientation=orientation)
        currentPos = move(pos=currentPos, orientation=orientation)
        resultpath = resultpath + (currentPos,)

    else:
        # this is what's happening if there's a wall to the left
        if not is_frontwall:
            # if there's no wall in front of us, we move without turning
            # and store our new position
            currentPos = move(pos=currentPos, orientation=orientation)
            resultpath = resultpath + (currentPos,)

        else:
            # this is what's happening if there's a wall to the left
            # and there's a wall in front of us. we simple turn
            # without moving and go the the next loop
            orientation = turn(orientation=orientation, clockwise=False)



    # this is just a safe guard counter to avoid infinite loops
    # if the code can't find the end position
    CURRENTITER += 1

    if CURRENTITER == MAXITER:
        print('==> REACHED ITERLIMIT !!! ---')
        break


t1 = time.time()
print("End Time: ", t1)
total = t1 -t0
print("Time Taken: ", total)
print('--> steps taken:', CURRENTITER)
# resultpath = (
#     (0, 3),
#     (1, 3),
#     (1, 4),
#     (1, 5),
#     (1, 6),
#     (1, 7),
#     (2, 7),
#     (3, 7),
#     )
print('\n\n===> STEPS:')
print(resultpath)

length = len(resultpath)
#print("Total Steps: ", length)

print ("Saving Image")
im = im.convert('RGB')
impixels = im.load()


# in this part here your boss just takes the collected list
# of steps we made, and set's pixel colour for a new image
# so he can save the solution to a new image so you can see
# what appened.
for i in range(0, length - 1):
    a = resultpath[i]
    b = resultpath[i+1]

    # Blue - red
    r = int((i / length) * 255)
    px = (r, 0, 255 - r)

    if a[0] == b[0]:
        # Ys equal - horizontal line
        for x in range(min(a[1],b[1]), max(a[1],b[1])):
            impixels[x,a[0]] = px
    elif a[1] == b[1]:
        # Xs equal - vertical line
        for y in range(min(a[0],b[0]), max(a[0],b[0]) + 1):
            impixels[a[1],y] = px

im.save(output_file)
print("Saved outputFile")
