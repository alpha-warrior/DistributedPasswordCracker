import hashlib

# list of all printable characters
printable = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`!@#$%^&*()_-+={[}]|\:;'<,>.?/" + '"'
allChars = list(printable)


"""
This function will be used by client to decode each number in the range provided to it to a string.
"""


def decode(allChars, inp):
    # inp+=1
    # this base is the base of number provided.
    base = len(allChars)
    ret = ""
    inp -= 1
    while inp >= 0:
        curr = inp % base
        ret = allChars[curr]+ret
        inp = inp//base-1
    return ret


def funcClient(interval, hash, type):
    """
    Iterates throught the interval provided by the server, for each number decodes it from integer, encoding it to bytes to be acceptable by hash function
    """
    global allChars
    # print(interval[0], interval[1])
    for i in range(interval[0], interval[1]+1):
        currStr = decode(allChars, i)  # Decoding the current integer
        # Hashing the string with given hashfunction
        # print(currStr)
        if type == 'sha':
            currHash = hashlib.sha256(currStr.encode())
            if currHash.hexdigest() == hash:  # comparing the hexdigest value of both the hashes
                return currStr
        elif type == 'md5':
            currHash = hashlib.md5(currStr.encode())
            if currHash.hexdigest() == hash:  # comparing the hexdigest value of both the hashes
                return currStr
            # print("The password is :", currStr, i)
    return ""

# interval = [0, 130]
# password = "abcd"
# hash = hashlib.sha256(password.encode())
# funcClient(interval,hash,allChars)
# fileAdd = "common_pass.txt"


def checkCommon(fileAdd, hash, allChars, type):
    """
    This function checks if the password is among the most common passwords.
    """

    f = open(fileAdd, 'r')

    for currStr in f:
        currStr = currStr[0:-1] # removing new line
        # Hashing the string with given hashfunction
        if type == 'sha':
            currHash = hashlib.sha256(currStr.encode())
            if currHash.hexdigest() == hash.hexdigest():  # comparing the hexdigest value of both the hashes
                print("The password is :", currStr)


# checkCommon(fileAdd, hash, allChars)
