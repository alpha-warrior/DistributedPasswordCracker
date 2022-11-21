import hashlib

password = input("Enter the password: ")
hashtype = input("Enter the hashtype: ")

if hashtype == 'sha':
    pswd_hash = hashlib.sha256(password.encode())
    print(pswd_hash.hexdigest())
    
else:
    pswd_hash = hashlib.md5(password.encode())
    print(pswd_hash.hexdigest())
    