import io
import socket
import struct
import time
from PIL import Image
from subprocess import call
import os

WIDTH = 50 #width of land that the picture takes in cm  -> TBD DURING TEST
HEIGHT = 54 #length of the land that the picture takes in cm  ->  TBD DURING TEST
SPEED = 11 #speed of robot in cm/sec -> TBD DURING TEST
COL = 2
ROW = 3
ROADlength = HEIGHT * 5

CELLwidth = int(40 / COL)
cellHeight = int(HEIGHT / ROW) #18
pixelW = 2880
pixelH = 2160
TOTALROW = int(ROADlength // cellHeight)
startLimitPixelX = int((WIDTH - (COL * CELLwidth))/2) #10
endLimitPixelX = int(WIDTH - (WIDTH - (COL * CELLwidth))/2) #40
matrix = [[0 for i in range(COL)] for j in range(TOTALROW)]
print(*matrix)
t2= time.time()
#delay = 0 #TBD in test case till server connects
#t0 = 3
#length = 196 # length of the are

def colorPicture(counter2, label, x1, x2, y1, y2):#function to call everytime you take a picture and get positions of weed or cabbage
    print("CheckList1")
    print(str(counter2))
    print(str(label))
    print(str(x1))
    print(str(x2))
    print(str(y1))
    print(str(y2))
    #t1 = time.time()
    #currentPosition = SPEED*(t1-t0)
    #currentRow = int(currentPosition / CELLwidth)
    
    print("CheckList2")
    realX1 = int((WIDTH * x1) / pixelW)
    realX2 = int((WIDTH * x2) / pixelW)
    realY1 = int((HEIGHT * y1) / pixelH)
    realY2 = int((HEIGHT * y2) / pixelH)
    
    print("CheckList3")
    if realX2 >= startLimitPixelX and realX1 <= endLimitPixelX :
        
        print("CheckList4")
        if realX1 <= startLimitPixelX :
            print("CheckList5")
            realX1 = startLimitPixelX + 0.01
        
        print("CheckList6")
        if realX2 >= endLimitPixelX :
            print("CheckList7")
            realX2 = endLimitPixelX - 0.01
        print("CheckList8")
        
        print("realX1 " + str(realX1) + "; realX2 " + str(realX2) + "; realY1 " + str(realY1) + "; realY2 " + str(realY2))
        
        X1 = int( (realX1 - startLimitPixelX) / CELLwidth)
        X2 = int( (realX2 - startLimitPixelX) / CELLwidth)
        Y1 = int(( realY1 / cellHeight )) #+  (counter2 - 1) * ROW
        Y2 = int(( realY2 / cellHeight )) #+ (counter2 - 1) * ROW )
        

        print("X1 " + str(X1) + "; X2 " + str(X2) + "; Y1 " + str(Y1) + "; Y2 " + str(Y2))
        
        print("CheckList9")
        for i in range(Y1,Y2+1):
            print("CheckList10")
            for j in range(X1, X2+1):
                print("CheckList11")
                if (label == -2):
                    print("CheckList12")
                    matrix[(counter2 - 1) * ROW + (ROW - 1 - i)][j] = -2
                elif label == -1 and matrix[(counter2 - 1) * ROW + (ROW - 1 - i)][j] != -2:
                    print("CheckList13")
                    matrix[(counter2 - 1) * ROW + (ROW - 1 - i)][j] = -1
        print("colorPicture Function ended")

"""
    this function returns a list including the nozzles needed to be activated.
    call this function over and over again while the robot is moving.The time
    interval according to which the function should be called will be determined
    based on the speed. TBD
    """
def spray(counter1):
    #print("Spray CheckList1")
    tempStr = ""
    #print("Spray CheckList2")
    #DELAY = 0 # delay till the sprayers reach starting position.
    #t1 = time.time() + DELAY
    #currentPosition = int(SPEED*(t1-t0))
    #currentRow = int(currentPosition // 7)
    #retList = []
    
    if counter1 == 1 :
        #print("Spray CheckList3")
        tempStr = tempStr + "0 0 0 0 0 0 "
        #print("Spray CheckList4")
        for i in range (1,ROW):
            #print("Spray CheckList5")
            for j in range (0, COL):
                #print("Spray CheckList6")
                if matrix[((counter1 - 1) * ROW + i)][j] != -1 :
                    #print("Spray CheckList7")
                    tempStr = tempStr + "0 0 0"
                else :
                    #print("Spray CheckList8")
                    tempStr = tempStr + "2 2 2"
                #print("Spray CheckList9")
                tempStr = tempStr + " "
    else :
        #print("Spray CheckList10")
        for i in range (0,ROW):
            #print("Spray CheckList11")
            for j in range (0, COL):
                #print("Spray CheckList12")
                if matrix[((counter1 - 1) * ROW + i)][j] != -1 :
                    #print("Spray CheckList13")
                    tempStr = tempStr + "0 0 0"
                else :
                    #print("Spray CheckList14")
                    tempStr = tempStr + "2 2 2"
                #print("Spray CheckList15")
                tempStr = tempStr + " "

    print("Spray Function ended")
    #return retList
    return tempStr

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
#t0 = time.time() + delay
connection = connection1.makefile('rb')
# connection1 address = server_socket.accept()
print("Connected to: " + address[0] + ":" + str(address[1]))
count = 0
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
        
        count = count + 1
        imageName1 = "t/" + str(count) + 'out.jpeg'
        imageName2 = str(count) + 'out.jpeg'
        
        image = Image.open(image_stream).save(imageName2)
        
        pathname = "./darknet detector test cfg/READY.data cfg/READY.cfg backup/READY_20000.weights " + imageName1 + " -thresh 0.05"
        call([pathname],shell = True)
        
        try:
            with open('text1.txt') as f:
                mylist = f.read().splitlines() #below if line should be in loop
                print("size of mylist: " + str(len(mylist)))
                if len(mylist) > 0 :
                    print(*mylist)
                    k = 0
                    while k < len(mylist) :
                        print("1 => Check for counter = " + str(count) + " and k = " + str(k))
                        afterK = int(mylist[k + 1])
                        print("afterK = " + str(afterK))
                        if afterK >= 0:
                            #colorPicture(str(mylist[0]), int(mylist[1]), int(mylist[2]), int(mylist[3]), int(mylist[4]))
                            print("2 => Check for counter = " + str(count) + " and k = " + str(k))
                            colorPicture(int(count), int(mylist[k]), int(mylist[k + 1]), int(mylist[k + 2]), int(mylist[k + 3]), int(mylist[k+4]))
                            print(*matrix)
                        else :
                            print("2 => Check for counter = " + str(count) + " and k = " + str(k))
                            k = k + 1
                            colorPicture(int(count), int(-2), int(mylist[k + 1]), int(mylist[k + 2]), int(mylist[k + 3]), int(mylist[k + 4]))
                        k = k + 5

                    print("FULL MATRIX AFTER IMAGE " + str(count) + "=> ") #*matrix)
                    spraylist = spray(int(count))
                    #spraylist = "2 2 0 0 0 0 " + "0 0 0 0 0 0 " + "0 0 0 0 0 0 "
                    #spraylist = "2 2 2 0 0 0 " + "0 0 0 2 2 2 " + "2 2 2 2 2 2 "
                    print(str(spraylist))
                    connection1.send(str.encode(spraylist)) #!!! NEED TO CONVERT TO STR
                    #connection1.send(str.encode(strArray))
                
                    print("Check Last")
                    print(str(count) + '. Data was sent!\n')
                else :
                    connection1.send(str.encode("No Object determined -> NO INPUT"))
                    print(str(count) + ". No Object determined -> NO INPUT")
        except:
            print(str(count) + '. File could not open. No such a file.')
            connection1.send(str.encode("NO INPUT. Entered Exception"))
    
        pathname1 = "mv predictions.jpg predictions" + str(count) + ".jpg"
        call([pathname1],shell = True)
        
        print(str(count) + '. Image is verified')
        print(str(count) + '. Data could not be sent!\n')

        #print('Image is %dx%d' % image.size)
        #image.verify()
finally:
    connection.close()
    server_socket.close()
