import hashlib
import random

import datetime

number = '221784269198'
datetime_str = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
spice = str(random.randint(1000,20000))

content = number + datetime_str + spice

print(hashlib.sha1(content.encode()).hexdigest())

