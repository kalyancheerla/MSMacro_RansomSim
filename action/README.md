### OpenSSL commands to generate RSA Keys
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:4096\
openssl rsa -pubout -in private_key.pem -out public_key.pem


### Windows settings
install python3\
install action requirements in venv (pycryptodome, pyinstaller)\
gen encrypt.exe (pyinstaller --onefile encrypt.py)\
encrypt files

Enable external script execution in powershell through admin access\
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

Disable all virus and threat protection settings in Windows defender
