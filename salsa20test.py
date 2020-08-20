from Crypto.Cipher import Salsa20

plaintext = b'Iamcute'
secret = b'*Thirty-two byte (256 bits) key*'

cipher = Salsa20.new(key=secret)
msg = cipher.nonce + cipher.encrypt(plaintext)
print(cipher.nonce)
print(plaintext)
print(msg)
print('\n')

msg = str(msg)
print(msg)
msg = bytearray(msg.strip('\'').strip('b'), encoding = 'utf-8')
print(msg)
print('\n')

msg_nonce = msg[:8]
ciphertext = msg[8:]
print(msg_nonce)
print(ciphertext)
cipher = Salsa20.new(key=secret, nonce=msg_nonce)
plaintext = cipher.decrypt(ciphertext)
print(plaintext.decode())
