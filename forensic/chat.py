import socket
import thread
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

CHAT_HEADER = '--SECCHAT_START--\n'
CHAT_FOOTER = '\n--SECCHAT_END--'
MY_PROMPT = ''
REMOTE_PROMPT = '[Rmt]>>> '

def recv_until(conn, str):
	buf = ''

	while not str in buf:
		buf += conn.recv(1)

	return buf

def chat_listen(conn, privatekey):
	print '[+] Listen session started'

	while True:
		data = recv_until(conn, CHAT_FOOTER)
		enc_msg = data[len(CHAT_HEADER):-(len(CHAT_FOOTER))]
		print REMOTE_PROMPT + privatekey.decrypt(enc_msg)

def chat_write(conn, remote_pubkey):
	print '[+] Write session started'

	while True:
		raw = raw_input(MY_PROMPT)
		encrypted = remote_pubkey.encrypt(raw, 32)[0]
		conn.send(CHAT_HEADER + encrypted + CHAT_FOOTER)

def key_exchange_listen(myport):
	s = socket.socket()
	s.bind(('', myport))
	s.listen(1)
	print '[?] Waiting for connection...'

	conn,addr = s.accept()
	raw_pubkey = recv_until(conn, '-----END PUBLIC KEY-----')
	remote_pubkey = RSA.importKey(raw_pubkey)

	print '[+] Remote public key received from ' + str(addr)

	chat_write(conn, remote_pubkey)
	return

def key_exchange_write(addr, port, publickey, privatekey):
	conn = socket.socket()

	while True:
		try:
			conn.connect((addr, port))
			break
		except:
			time.sleep(1)
			pass

	print '[+] Connection established with ' + str(addr)
	conn.send(publickey.exportKey(format='PEM') + '\n')
	print '[+] Public key sent'

	chat_listen(conn, privatekey)
	return

def main():
	key = RSA.importKey(open('myprivatekey.pem','r').read())

	myport = int(raw_input('Enter My Port: '))
	ip = raw_input('Enter Remote IP: ')
	remote_port = int(raw_input('Enter Remote Port: '))

	thread.start_new_thread(key_exchange_write,(ip, remote_port, key.publickey(), key))
	thread.start_new_thread(key_exchange_listen,(myport,))

	while 1:
		pass

if __name__ == "__main__":
	main()