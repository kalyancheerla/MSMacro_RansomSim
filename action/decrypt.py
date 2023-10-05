#!/usr/bin/env python3
import os, sys
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

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

""" Do RSA Decryption """
def rsa_decrypt(encrypted_data, private_key_file):
    # import private key
    with open(private_key_file, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())
    # get cipher
    cipher = PKCS1_OAEP.new(private_key)
    # return decrypted data
    return cipher.decrypt(encrypted_data)


""" Decrypt each file """
def decrypt_file(private_key_file, in_filename):
    # remove '.enc' extension for the decrypted file
    out_filename = in_filename[:-4]
    with open(in_filename, 'rb') as infile:
        # extract nonce which is first 8bytes
        nonce = infile.read(8)
        # extract 512bytes of encrypted 32bytes aes key using rsa:4096
        encrypted_aes_key = infile.read(512)

        # get aes key
        aes_key = rsa_decrypt(encrypted_aes_key, private_key_file)
        # perform aes decryption
        cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)

        # write to file
        with open(out_filename, 'wb') as outfile:
            outfile.write(cipher.decrypt(infile.read()))

""" Perform the decryption of folder recursively """
def perform_folder_decryption(private_key_file, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                # get file name with folder path
                in_filename = os.path.join(root, file)
                # decrypt the file
                decrypt_file(private_key_file, in_filename)
                # securely delete the encrypted file after decryption
                secure_delete(in_filename)

""" Decrypt Usage """
def usage():
    print("./decrypt.py <folder path 1> <folder path 2>... <private key file>")

""" MAIN FUNCTION """
def main(argv):
    if len(argv) < 2:
        usage()
        sys.exit(1)

    folders = argv[:len(argv)-1]
    private_key_file = argv[-1]

    # recursively perform for all folders
    for folder_path in folders:
        perform_folder_decryption(private_key_file, folder_path)

    print("Decryption was successfully completed!")

if __name__ == "__main__":
    main(sys.argv[1:])

