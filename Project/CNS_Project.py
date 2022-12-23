# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 23:42:59 2021

@author: M Sabbagh
"""


from hashlib import sha256
import json
from backports.pbkdf2 import pbkdf2_hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
from base64 import b64decode



def salt_hash(username, password):
    
    usalt = sha256(username.encode()).hexdigest()
    psalt = sha256(password.encode()).hexdigest()
    username = username + usalt
    password = password + psalt
    hashed_username = sha256(username.encode()).hexdigest()
    hashed_password = sha256(password.encode()).hexdigest()
    return hashed_username, hashed_password

def duplicate(passdic, username, password):
    if username in passdic:
        return 1
    elif password in passdic.values():
        return 1
    else:
        return 0
    
        
def create(username, password):
    
    YN = 1
    
    while YN == 1:
        
        hashed_username, hashed_password = salt_hash(username, password)
        
        file = open("database.txt", "r")
        passdic = json.loads(file.read())
        file.close()
        
        file = open("number.txt", "r")
        numdic = json.loads(file.read())
        file.close()
        
        YN = duplicate(passdic, hashed_username, hashed_password)
        
        if YN == 0:
            
            num = numdic["number"]
            num = num + 1
            
            numdic["number"] = num
            numdic[hashed_username] = num
            passdic[hashed_username] = hashed_password
            
            file = open("number.txt", "w")
            json.dump(numdic, file)
            file.close()
            
            file = open("database.txt", "w")
            json.dump(passdic, file)
            file.close()
            
            dic = {}
            filename = str(num) + '.txt' 
            file = open(filename, "w")
            json.dump(dic, file)
            file.close()
            
            salt = sha256((username + password).encode()).hexdigest()
            mkey = pbkdf2_hmac("sha256", password.encode('utf-8'), salt.encode('utf-8'), 50000, 32)
            fnum = numdic[hashed_username]

            print("\nWelcome!")
            break
        
        print('\nYour username or password is already taken. Please enter a new username:')
        username = input()
        print('\nand a new password:')
        password = input()
        
    return mkey, fnum

def signin(username, password):
    
    while True:
        hashed_username, hashed_password = salt_hash(username, password)
        
        file = open("database.txt", "r")
        passdic = json.loads(file.read())
        file.close()
        
        file = open("number.txt")
        numdic = json.loads(file.read())
        file.close()
        
        
        if hashed_username in passdic:
            if passdic[hashed_username] == hashed_password :
                salt = sha256((username + password).encode()).hexdigest()
                mkey = pbkdf2_hmac("sha256", password.encode('utf-8'), salt.encode('utf-8'), 50000, 32)
                fnum = numdic[hashed_username]
                print("\nWelcome!")
                break
            else:
                print("\nError: Wrong password! Try again.")
        else:
            print("\nError: Username is wrong! Try again.")
                
        print("\nEnter username:")
        username = input()
        print("\nEnter password:")
        password = input()
            
    return mkey, fnum


def addkeyvalue(mkey, fnum):
    
    print("\nEnter new domain service:")
    key = input()
    print("\nEnter password of domain service:")
    value = input()
    
    key = key.encode('utf-8')
    value = value.encode('utf-8')
    
    key = pad(key, 64)
    value = pad(value, 64)
    
    obj = AES.new(mkey, AES.MODE_ECB)
    key = obj.encrypt(key)
    value = obj.encrypt(value)
    
    key = b64encode(key).decode('utf-8')
    value = b64encode(value).decode('utf-8')
    
    filename = str(fnum) + '.txt'
    
    file = open(filename, "r")
    dic = json.loads(file.read())
    file.close()
    
    if key in dic:
        print("\nError: Domain service already exists!")
    else:
        dic[key] = value
        
        file = open(filename, "w")
        json.dump(dic, file)
        file.close()
        
        print("\nNew domain service and password added successfully.")
        
    
def getpass(username, password, mkey, fnum):    
    
    print("\nEnter domain service:")
    key = input()
    
    key = key.encode('utf-8')
    
    key = pad(key, 64)
    
    obj = AES.new(mkey, AES.MODE_ECB)
    key = obj.encrypt(key)
    
    key =  b64encode(key).decode('utf-8')
    
    filename = str(fnum) + '.txt'
    
    file = open(filename, "r")
    dic = json.loads(file.read())
    file.close()
    
    if key in dic:
        value = dic[key]
        value = b64decode(value)
        value = obj.decrypt(value)
        value = unpad(value, 64).decode('utf-8')
        print("\nThe desired password is: ", value)
    else:
        print("\nError: The domain service is not defined!")
        
def changedomainpass(username, password, mkey, fnum):
    
    print("\nEnter domain service:")
    key = input()
    print("\nEnter new password of domain service:")
    value = input()
     
    key = key.encode('utf-8')
    value = value.encode('utf-8')
    
    key = pad(key, 64)
    value = pad(value, 64)
    
    obj = AES.new(mkey, AES.MODE_ECB)
    key = obj.encrypt(key)
    value = obj.encrypt(value)
    
    key =  b64encode(key).decode('utf-8')
    value = b64encode(value).decode('utf-8')
    
    filename = str(fnum) + '.txt'
    
    file = open(filename, "r")
    dic = json.loads(file.read())
    file.close()
    
    if key in dic: 
        dic[key] = value
        
        file = open(filename, "w")
        json.dump(dic, file)
        file.close()
        print("\nPassword changed successfully.")
        
    else:
        print("\nError: The domain service is not defined!")
        
    

def changeuserpass(username, password, mkey, fnum):
    
    print("\nEnter new username:")
    newuser = input()
    print("\nEnter new password:")
    newpass = input()
    
    hashed_username, hashed_password = salt_hash(username, password)
    hashed_newuser, hashed_newpass = salt_hash(newuser, newpass)
    
    file = open("database.txt", "r")
    passdic = json.loads(file.read())
    file.close()
        
    file = open("number.txt", "r")
    numdic = json.loads(file.read())
    file.close()
    
    while True:
        if (hashed_newuser in passdic) and (hashed_newuser != hashed_username):
            print("\nError: Username is already taken. Please enter a new username:")
            newuser = input()
        else:
            break
    
    while True:  
        if (hashed_newpass in passdic.values()) and (passdic[hashed_username] != hashed_newpass):
    
            print("\nError: Password is already taken. Please enter a new password:")
            newpass = input()
        else:
            break
        
     
    passdic[hashed_newuser] = hashed_newpass
    del passdic[hashed_username]
    
    numdic[hashed_newuser] = numdic[hashed_username]
    del numdic[hashed_username]
    
    file = open("number.txt", "w")
    json.dump(numdic, file)
    file.close()
            
    file = open("database.txt", "w")
    json.dump(passdic, file)
    file.close()
    
    newsalt = sha256((newuser + newpass).encode()).hexdigest()
    newmkey = pbkdf2_hmac("sha256", newpass.encode('utf-8'), newsalt.encode('utf-8'), 50000, 32)
    
    newobj = AES.new(newmkey, AES.MODE_ECB)
    
    newdic = {}
    
    filename = str(fnum) + '.txt'
    
    file = open(filename, "r")
    dic = json.loads(file.read())
    file.close()
    
    obj = AES.new(mkey, AES.MODE_ECB)
    
    for key in dic:
        value = dic[key]
        value = b64decode(value)
        value = obj.decrypt(value)
        value = unpad(value, 64).decode('utf-8')
        
        key = b64decode(key)
        key = obj.decrypt(key)
        key = unpad(key, 64).decode('utf-8')
        
        key = key.encode('utf-8')
        value = value.encode('utf-8')
    
        key = pad(key, 64)
        value = pad(value, 64)
    
        key = newobj.encrypt(key)
        value = newobj.encrypt(value)
    
        key = b64encode(key).decode('utf-8')
        value = b64encode(value).decode('utf-8')
        
        newdic[key] = value
        
    file = open(filename, "w")
    json.dump(newdic, file)
    file.close()
        
    print("\nUsername and password changed successfully.")
        
    return newmkey
   
        
        
##############################################################################        

SC = 0

while (SC != '1' and SC != '2'):
    print("\nSign in (enter 1) or create an account (enter 2) ? ")
    SC = input()


print("\nEnter username:")
username = input()
print("\nEnter password:")
password = input()

if SC == '1':
    mkey, fnum = signin(username, password)
     
elif SC == '2':
    mkey, fnum = create(username, password)
    
logout = 0
while logout != 1:
    service = 0
    while (service != '1' and service != '2' and service != '3' and service != '4' and service != '5'):
        print("""\nAdd new domain service (enter 1) 
              \nGet password of a domain service (enter 2)
              \nChange password of a domain service(enter 3) 
              \nChange your username or account password (enter 4)
              \nLog out (enter 5)""")
        service = input()
    
        
    if service == '1':
        addkeyvalue(mkey, fnum)
          
    elif service == '2':
        getpass(username, password, mkey, fnum)
        
    
    elif service == '3':
        changedomainpass(username, password, mkey, fnum)
    
    elif service == '4':
        mkey = changeuserpass(username, password, mkey, fnum)
        
    elif service == '5':
        logout = 1
    
      
            
    
        