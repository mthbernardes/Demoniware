import sys
import clipboard
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from time import gmtime, strftime

if len(sys.argv) < 2:
	print 'Error'
	exit()

def save_keys(keys):
	print 'Saving Keys'
	open('private_key','w').write(keys.exportKey())
	open('public_key','w').write(keys.publickey().exportKey())
	print 'Keys Saved'


if sys.argv[1] == 'create':
	print 'Creating keyss'
	random_gen = Random.new().read
	print 'Keys created'
	keys = RSA.generate(1024, random_gen)
	save_keys(keys)

else:
	msg = sys.argv[1]
	keys = RSA.importKey(open('private_key').read())
	now = strftime("%Y-%m-%d %H:%M", gmtime())
	msg_final = msg+now
	msg_hash = SHA256.new(msg_final).digest()
	signature = keys.sign(msg_hash, '')[0]
	clipboard.copy(str(signature)+' '+msg)
	print 'Message copied to clipboard!'
