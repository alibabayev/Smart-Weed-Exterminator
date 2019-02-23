import io
import socket
import struct
import time
from PIL import Image
from subprocess import call
import os

host = ''
port = 8000
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

        pathname = "./darknet detector test cfg/READY.data cfg/READY.cfg backup/READY_20000.weights " + imageName + " -thresh 0.05"

        call([pathname],shell = True)
        try:
            with open('text1.txt') as f:
                mylist = f.read().splitlines()
        except:
            print('File could not open. No such a file.')
        reply = 'l ' + mylist[0] + ' r ' + mylist[1] + ' t ' + mylist[2]+ ' b ' + mylist[3]

        #print('Image is %dx%d' % image.size)
        #image.verify()
        print('Image is verified')
        connection1.send(str.encode(reply))
        print('Data has been sent!\n')

        count = count + 1
finally:
    connection.close()
    server_socket.close()
