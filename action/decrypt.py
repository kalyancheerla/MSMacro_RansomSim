#!/usr/bin/env python3
import os
import sys
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

""" Securely delete the file after writing random bytes in it. """
def secure_delete(filename):
    with open(filename, "ba+") as delfile:
        # get the file length
        length = delfile.tell()
        # write random bytes in the file
        delfile.seek(0)
        delfile.write(get_random_bytes(length))
    # remove the file
    os.remove(filename)

""" Decrypt each file """
def decrypt_file(key, in_filename):
    # remove '.enc' extension for the decrypted file
    out_filename = in_filename[:-4]
    with open(in_filename, 'rb') as infile:
        # extract nonce which is first 8bytes
        nonce = infile.read(8)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        with open(out_filename, 'wb') as outfile:
            outfile.write(cipher.decrypt(infile.read()))

""" Perform the decryption of folder recursively """
def perform_folder_decryption(key, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                # get file name with folder path
                in_filename = os.path.join(root, file)
                # decrypt the file
                decrypt_file(key, in_filename)
                # securely delete the encrypted file after decryption
                secure_delete(in_filename)

""" Decrypt Usage """
def usage():
    print("./decrypt.py <folder path 1> <folder path 2>... <password>")

""" MAIN FUNCTION """
def main(argv):
    if len(argv) < 2:
        usage()

    folders = argv[:len(argv)-1]
    password = argv[-1]

    # Use SHA256 to derive key for AES
    key = SHA256.new(password.encode()).digest()

    # recursively perform for all folders
    for folder_path in folders:
        perform_folder_decryption(key, folder_path)

    print("Decryption was successfully completed!")

if __name__ == "__main__":
    main(sys.argv[1:])

