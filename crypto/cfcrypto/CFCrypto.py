import os, copy

class Block:
	_BLOCK_SIZE = 16

	def __init__(self, key, IV, rounds):
		self.key = [ord(c) for c in self._pad(key)]
		self.IV  = [ord(c) for c in self._pad(IV) ]
		self.rounds = rounds

	def __str__(self):
		return str({'key':self.key, 'IV':self.IV, 'rounds':self.rounds})

	def encrypt(self, msg):
		msg = [ord(c) for c in self._pad_zero(msg)]
		
		block_cnt = len(msg)/self._BLOCK_SIZE
		blocks = []
		enc = []
		DV = self.IV

		for i in range(block_cnt):
			blocks.append( msg[i*self._BLOCK_SIZE : (i+1)*self._BLOCK_SIZE] )

		for i in range(block_cnt): 
			_block = self._xor(blocks[i], DV)
			_block = self._encrypt_block(_block)
			
			DV = _block
			enc += _block

		return "".join([chr(c) for c in enc])

	def decrypt(self, enc):
		enc = [ord(c) for c in enc]
		
		block_cnt = len(enc)/self._BLOCK_SIZE
		blocks = []
		msg = []
		DV = self.IV

		for i in range(block_cnt):
			blocks.append( enc[i*self._BLOCK_SIZE : (i+1)*self._BLOCK_SIZE] )

		for i in range(block_cnt):
			_block = self._decrypt_block(blocks[i])
			msg += self._xor(_block, DV)

			DV = blocks[i]

		return "".join([chr(c) for c in msg])


	# Privates
	# --------------

	def _pad(self, s):
		cnt = self._BLOCK_SIZE - (len(s) % self._BLOCK_SIZE)
		if cnt == self._BLOCK_SIZE: cnt = 0

		return s + os.urandom(cnt)

	def _pad_zero(self, s):
		cnt = self._BLOCK_SIZE - (len(s) % self._BLOCK_SIZE)
		if cnt == self._BLOCK_SIZE: cnt = 0

		return s + ('\x00' * cnt)

	def _shiftL(self, ls):
		return ls[1:] + ls[:1]

	def _shiftR(self, ls):
		return ls[-1:] + ls[:-1]

	def _xor(self, m1, m2):
		_msg = []

		for i in range(len(m1)):
			_msg.append(m1[i] ^ m2[i])

		return _msg

	def _encrypt_block(self, msg):
		for i in range(0, self.rounds):
			msg = self._xor(msg, self.key)
			msg = self._shiftL(msg)

		return msg

	def _decrypt_block(self, msg):
		_msg = copy.deepcopy(msg)

		for i in range(0, self.rounds):
			_msg = self._shiftR(_msg)
			_msg = self._xor(_msg, self.key)

		return _msg


if __name__ == '__main__':
	pass