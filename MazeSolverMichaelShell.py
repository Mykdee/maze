from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000
import time

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



while True:

    """
    Michael put your movement code here

    """

    # Dont for get to change this to something that sets completed to True
    if currentPos == endcoord:
        break
        print("Found The Exit")


t1 = time.time()
print("End Time: ", t1)
total = t1 -t0
print("Time Taken: ", total)

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
