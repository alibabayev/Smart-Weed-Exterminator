import io
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('169.254.145.159', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (720, 540)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    count = 0
    startTime = time.time()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 10:
            break
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        reply = client_socket.recv(1024)
        print(reply.decode('utf-8'))
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()

        endTime = time.time() - startTime
        print(endTime)
        count = count + 1
        startTime = time.time()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()