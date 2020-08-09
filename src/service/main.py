# Python for Android Service - connect to 7688 socket
'''import socket

host='192.168.43.89'
port=502

if __name__ == '__main__':
	so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	so.connect((host, port))
	so.sendall(b'Hello Steven, This message is sent by Android Service.')

	resp = str(so.recv(1024), encoding='utf-8')
	print("resp: %s" % resp)

	so.close()'''

print("Hello world from Android Background Service...")
