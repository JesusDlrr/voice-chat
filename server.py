# import socket, cv2, pickle,struct,time
# import pyshine as ps
import threading
import socket
import pyaudio as pa
import wave
import random
import struct

# mode =  'send'
# name = 'SERVER TRANSMITTING AUDIO'
# audio,context= ps.audioCapture(mode=mode)
#ps.showPlot(context,name)

HOST = '192.168.1.205'
PORT = 1369
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
FORMAT = 'utf-8'
N_CHANNELS = 2

audio = pa.PyAudio()
exit_signal = threading.Event()

SERVER.bind((HOST, PORT))


def handle_client(connection, address):
	print(f"[NEW CONNECTION]: {address} connected")
	
	connected = True

	while connected:
		audio_frame = bytearray(connection.recv(1024*N_CHANNELS+1))

		if(audio_frame[-1] == 0x00):
			connection.send(bytes(audio_frame[:-1]))
		else:
			connected = False
			print(f"[{connection}] disconnected")

	# stream.stop_stream()
	# stream.close()
	connection.close()


def start():
	SERVER.listen()
	
	try:
		while True:
			connection, address = SERVER.accept()
			thread = threading.Thread(target=handle_client, args=(connection, address))
			thread.start()
	except KeyboardInterrupt:
			SERVER.close()
	

print("Server is starting...")
start()
