from scrambler import Scrambler
from commons import *

scrambler = Scrambler.create_random()
msg = read("msg.txt")
key = read("key.key")