from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000
import time


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

data = list(im.getdata(0))

listMap = []
rowList = []
rowCount = 0
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

initcoord = (0, startPos)
endcoord = (height-1, endPos)
currentPos = initcoord
orientation = 'south'
resultpath = (initcoord,)
is_leftwall = None
is_frontwall = None


def check_left_wall(pos, orientation):
    if orientation == 'north':
        leftcoord = pos[0], pos[1]-1
    elif orientation == 'south':
        leftcoord = pos[0], pos[1]+1

    elif orientation == 'east':
        leftcoord = pos[0]+1, pos[1]
    elif orientation == 'west':
        leftcoord = pos[0]-1, pos[1]

    try:
        result = not bool(listMap[leftcoord[0]][leftcoord[1]])
    except:
        result = True

    return result



def check_front_wall(pos, orientation):
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



while True:

    """
    Michael put your movement code here

    """
    is_leftwall = check_left_wall(
        pos=currentPos, orientation=orientation)
    is_frontwall = check_front_wall(
        pos=currentPos, orientation=orientation)

    print('\n--> current pos:', currentPos)
    print('--> orientation:', orientation)
    print('--> is wall to left:', is_leftwall)
    print('--> is wall to front:', is_frontwall)

    # Dont for get to change this to something that sets completed to True
    if currentPos == endcoord:
        break
        print("Found The Exit")


    if not is_leftwall:
        orientation = turn(orientation=orientation)
        currentPos = move(pos=currentPos, orientation=orientation)
        resultpath = resultpath + (currentPos,)

    else:
        if not is_frontwall:
            currentPos = move(pos=currentPos, orientation=orientation)
            resultpath = resultpath + (currentPos,)

        else:
            orientation = turn(orientation=orientation, clockwise=False)



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
