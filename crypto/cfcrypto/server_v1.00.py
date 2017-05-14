import CFCrypto
import os, sys, time, base64

def print_(s):
	sys.stdout.write(s)
	sys.stdout.flush()

def println(s):
	print_(s + '\n')

def welcome():
	println( '==================================================\n'
		     '|           CompFest Crypto Demo v1.00           |\n'
		     '|                                                |\n'
		     '|    Changelog : - Initial Release               |\n'
		     '==================================================' )	

def menu():
	print_( '\n[+] Menu:\n'
			'  [1] Generate new encryptor\n'
			'  [2] Encrypt\n'
			'  [3] Get flag\n'
			'  [Other] Exit\n'
			'[?] Choice: ' )

	return raw_input()

def gen_enc(key):
	allowed_rounds = [3, 5, 8, 10, 14, 15]
	print_('  [?] Rounds : ')
	round = int(raw_input())

	if round in allowed_rounds:
		IV = os.urandom(16)
		return CFCrypto.Block(key, IV, round)
	else:
		println("  [!] Invalid rounds")
		return None

def pad():
	return os.urandom(16)

def encrypt_menu(enc):
	if enc == None:
		return '  [!] Encryptor not initialized'
	
	print_('  [?] Message: ')
	s = raw_input()
	return '  [+] Enc: ' + base64.b64encode( enc.encrypt(pad() + s) )

def get_flag(enc, s):
	if enc == None:
		return '  [!] Encryptor not initialized'

	return '  [+] Enc: ' + base64.b64encode( enc.encrypt(pad() + s) )

def main():
	welcome()

	# TODO : Replace this shrugging face with real flag.
	message = "¯\_(ツ)_/¯"
	key	  	= os.urandom(16)
	enc 	= None

	while True:
		i = menu()
		
		if i == '1':
			enc = gen_enc(key)
		elif i == '2':
			println( encrypt_menu(enc) )
		elif i == '3':
			println( get_flag(enc, message) )
		else:
			break

if __name__ == '__main__':
	main()