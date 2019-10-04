import io
import socket
import struct
import time
from PIL import Image
from subprocess import call
import os

WIDTH = 51 #width of land that the picture takes in cm  -> TBD DURING TEST
HEIGHT = 60 #length of the land that the picture takes in cm  ->  TBD DURING TEST
SPEED = 20 #speed of robot in cm/sec -> TBD DURING TEST
COL = 3
ROW = 3

CELLwidth = 11
pixelW = 720
pixelH = 540
cellHeight = 20
TOTALROW = int(240 // cellHeight)
startLimitPixelX = int((WIDTH - (COL * CELLwidth))/2)
endLimitPixelX = int(WIDTH - (WIDTH - (COL * CELLwidth))/2)
picture = [[0 for i in range(COL)] for j in range(TOTALROW)]
t2= time.time()
delay = 0 #TBD in test case till server connects
t0 = 3
length = 196 # length of the are

def colorPicture(counter2, label, x1, x2, y1, y2):#function to call everytime you take a picture and get positions of weed or cabbage
    #t1 = time.time()
    #currentPosition = SPEED*(t1-t0)
    #currentRow = int(currentPosition / CELLwidth)
    realX1 = int((WIDTH * x1) / pixelW)
    realX2 = int((WIDTH * x2) / pixelW)
    realY1 = int((HEIGHT * y1) / pixelH)
    realY2 = int((HEIGHT * y2) / pixelH)
    
    if realX2 >= startLimitPixelX && realX1 =< endLimitPixelX :
        if realX1 < startLimitPixelX :
            realX1 = startLimitPixelX
        
        if realX2 > endLimitPixelX :
            realX2 = endLimitPixelX
        
        X1 = int( realX1/ CELLwidth)
        X2 = int( realX2 / CELLwidth)
        Y1 = int(( realY1 // cellHeight ) + (counter-1) * 3)
        Y2 = int(( realY2 // cellHeight ) + (counter-1) * 3)
        
        for i in range(X1,X2+1):
            for j in range(Y1, Y2+1):
                if (label == "cabbage"):
                    picture[i][j] = -1
                elif (label == "mint" && picture[i][j] != -1):
                    picture[i][j] = -2
        print("colorPicture Function ended")

"""
    this function returns a list including the nozzles needed to be activated.
    call this function over and over again while the robot is moving.The time
    interval according to which the function should be called will be determined
    based on the speed. TBD
    """
def spray(counter1):
    tempStr = ""
    #DELAY = 0 # delay till the sprayers reach starting position.
    #t1 = time.time() + DELAY
    #currentPosition = int(SPEED*(t1-t0))
    #currentRow = int(currentPosition // 7)
    retList = []
    for i in range (0, ROW):
        for j in range (0, COL):
            if (picture[(counter-1) * 3 + i)][j] != -2 :
                tempStr = tempStr + "0"
            else :
                tempStr = tempStr + "2"
            tempStr = tempStr + " "
                #retList.append(i)

    print("spray Function ended")
    return retList


host = ''
port = 9000

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((host, port))
except socket.error as msg:
    print(msg)
print("Socket bind complete.")
server_socket.listen(1)
#reply = ""

# Accept a single connection and make a file-like object out of it
#connection = server_socket.accept()[0].makefile('rb')
connection1, address = server_socket.accept()
t0 = time.time() + delay
connection = connection1.makefile('rb')
# connection1 address = server_socket.accept()
print("Connected to: " + address[0] + ":" + str(address[1]))
count = 1
try:
    while True:
        
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        
        imageName = "t/" + str(count) + 'out.jpeg'
        
        image = Image.open(image_stream).save(imageName)
        
        pathname = "./darknet detector test cfg/READY.data cfg/READY.cfg backup/READY_25000.weights " + imageName + " -thresh 0.05"
        
        call([pathname],shell = True)
        try:
            with open('text1.txt') as f:
                mylist = f.read().splitlines() #below if line should be in loop
                print("size of mylist: " + str(len(mylist)))
                if len(mylist) > 0 :
                    print(*mylist)
                    for i in range(len(mylist)) :
                        if int(mylist[i+1]) >= 0 :
                            #colorPicture(str(mylist[0]), int(mylist[1]), int(mylist[2]), int(mylist[3]), int(mylist[4]))
                            colorPicture(counter, str(mylist[i]), int(mylist[i+1]), int(mylist[i+2]), int(mylist[i+3]), int(mylist[i+4]))
                            i  = i + 4
                        else :
                            i = i + 1
                    
                    spraylist = spray(counter)
                    strArray = "0 0 2 0 0 0 " + "0 0 0 2 0 0 " + "0 0 0 0 2 0 "
                    #for m in range(0, len(spraylist)-1):
                    
                    #print(*spraylist)
                    #connection1.send(str.encode(spraylist)) !!! NEED TO CONVERT TO STR
                    connection1.send(str.encode(strArray))
                    print("Check 7")
                    print(str(count) + '. Data was sent!\n')
                else :
                    connection1.send(str.encode("No Object determined -> NO INPUT"))
                    print(str(count) + ". No Object determined -> NO INPUT")
        except:
            print(str(count) + '. File could not open. No such a file.')
            connection1.send(str.encode("NO INPUT"))

        print(str(count) + '. Image is verified')
        print(str(count) + '. Data could not be sent!\n')
        picture = [[0 for i in range(COL)] for j in range(TOTALROW)]

        #print('Image is %dx%d' % image.size)
        #image.verify()
        count = count + 1
finally:
    connection.close()
    server_socket.close()
