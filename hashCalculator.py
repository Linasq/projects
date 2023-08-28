import hashlib

#main function
def start():
    try:
        print('Hello there!\nWhat do you want to do?')
        getInput = int(input('1. Create Hash of string\n2. Create hash of a file\n3. List available hash algorithms\n'))

        if getInput == 1:
            text = input('Input your text you want to be hashed:\n')
            wHash = input('What hash algorithm do you want to use?\n')

            hashString(text, wHash)

        elif getInput == 2:
            directory = input('Enter absolute path to this file:\n')
            wHash = input('What hash algorithm do you want to use?\n')

            hashFile(directory, wHash)

        elif getInput == 3:
            printHashes() 

        else:
            print('Wrong number, try again...\n')
            start()

    except:
        print('Wrong input value, try using integers\n')
        start()
    
    
#calculate hash of string
def hashString(text, wHash):
    try:
        h = hashlib.new(wHash)
        inBytes = str.encode(text)
        h.update(inBytes)
        print()
        print('Here is your hash:')
        print(h.hexdigest())
        print()
    except:
        print('Wrong hash name\nLearn hash algorithms then come back\nBye')
        exit()

#calculate hash of file
def hashFile(directory, wHash):
    try:
        with open(directory, 'rb') as f:
            digest = hashlib.file_digest(f, wHash)
            print('Here is your hash:\n')
            print(digest.hexdigest())
            print()
    except:
        print('Wrong directory or hash value\nBye')
        exit()
        

def printHashes():
    print('''This is list of hash algorithms:
              - md5
              - sha1
              - sha224
              - sha256
              - sha384
              - sha512
              - sha3_224
              - sha3_256
              - sha3_384
              - sha3_512

Use these names when you will be asked for hash algorithm\n''')
    start()


start()
