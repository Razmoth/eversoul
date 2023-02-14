from sys import argv
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

VERSION = 1065 #optained from API/table
ZIPHASH = '#Rk@Lw+Ap'
JSONHASH = '!@UmWlXo'
OUTPUT = Path('files')

def to_int32(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000

def generate_key(version, hash):
    h = to_int32(version ^ 0x80000000)
    h = f"{h}{hash}".encode('utf-8')
    h = sha256(h)
    return h.digest()

def get_password():
    return generate_key(VERSION, ZIPHASH).decode('utf-16', 'replace').encode('utf-8')

def get_key():
    return generate_key(VERSION, JSONHASH)[:0x10]

def write_to_file(name, data):
    print(f"Writing {name} to {OUTPUT}...")

    if not OUTPUT.exists():
        OUTPUT.mkdir()
        
    with open(f"./files/{name}", 'wb') as file:
        file.write(data)

    print(f"{name} extracted !!")

def extract_zip_file(path):
    print('Extracting archive...')
    try:
        key = get_key()
        aes = AES.new(key, AES.MODE_CBC, key)
        with ZipFile(path) as zip:
            zip.setpassword(get_password())
            for info in zip.infolist():

                print(f"Reading {info.filename} from archive...")
                data = zip.read(info)

                print(f"Decrypting {info.filename}...")
                data = unpad(aes.decrypt(data), 0x10)
                
                write_to_file(info.filename, data)
                
    except Exception as e:
        print('Error:' +  str(e))


if __name__ == '__main__':
    if len(argv) != 2:
        print('No input archive !')
    
    path = Path(argv[1])

    if not path.exists():
        print('Invalid path')

    extract_zip_file(str(path))