#!/usr/bin/env python

import hashlib

DOORID = 'ojvtpuvg'

number_found = 0
counter = 0
password = ''

while number_found < 8:
    test_string = DOORID + str(counter)
    digest = hashlib.md5(test_string).hexdigest()
    if digest[0:5] == "00000":
        code = digest[5]
        print test_string, digest, code
        password += code
        number_found += 1
    counter += 1

print password
