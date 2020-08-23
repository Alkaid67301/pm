from Crypto.Cipher import Salsa20
import binascii

plaintext = b'testmessage'
secret = b'*Thirty-two byte (256 bits) key*'

cipher = Salsa20.new(key=secret)
msg = cipher.nonce + cipher.encrypt(plaintext)
print(cipher.nonce)
print(plaintext)
print(msg)
print('\n')

msg = msg.hex()
print(msg)
print(len(msg))
msg = binascii.unhexlify(msg)
print(msg)
print('\n')

msg_nonce = msg[:8]
ciphertext = msg[8:]
print(msg_nonce)
print(ciphertext)
cipher = Salsa20.new(key=secret, nonce=msg_nonce)
plaintext = cipher.decrypt(ciphertext)
print('testmessage'.encode('utf-8'))
print(plaintext.decode('utf-8'))
