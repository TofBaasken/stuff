# The python solution script for the Cyber Security Challenge Belgium 2015 challenge: NVISO Lottery

import cPickle as pickle
from random import WichmannHill
import base64
from pwn import *

#r = remote('cybersecuritychallenge.be', 10004);
r = remote('localhost', 55567)

# Just keep looping ...
while True:
	d = r.recvuntil("2. No")
	
    # If we've got a prize, we can stop
	if "your prize" in d:
		print d
		break
	
	while r.can_recv():
		r.recvline()
		
    # We want to continue playing
	r.sendline("1")
	data = r.recvline()
	print "Received: ", data
    
    # Decode the value
	data = data[16:len(data)-2]
	data = base64.b64decode(data)
	
	seed = pickle.loads(data)
	
    # And predict the number
	prng = WichmannHill()
	prng.setstate(seed)
	
    # Consume the output until we can enter our number
	while r.can_recv():
		r.recvline()

	nr = prng.randrange(0, 1000)
	print "Sending nr ", str(nr)
	r.sendline(str(nr))
	print "Received: ", r.recvline()