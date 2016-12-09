#!/usr/bin/env python

import hashlib

DOORID = 'ojvtpuvg'
# DOORID = 'abc'

number_found = 0
counter = 0
password = list('________')

def password_complete():
    for char in password:
        if char == '_':
            return False
    return True

while not password_complete():
    test_string = DOORID + str(counter)
    digest = hashlib.md5(test_string).hexdigest()
    if digest[0:5] == "00000":
        char_index = digest[5]
        if ord(char_index) in range(48, 56):
            int_index = int(char_index)
            if password[int_index] == '_':
                char_to_insert = digest[6]
                password[int_index] = char_to_insert
                number_found += 1
                print password
    counter += 1

print ''.join(password)
