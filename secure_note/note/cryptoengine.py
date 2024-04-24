import rsa
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class MessageDigest:
    @staticmethod
    def md5_hash(message : str) ->  str:
        cipher = hashlib.md5()
        cipher.update(message.encode())
        return cipher.hexdigest()
    
    @staticmethod
    def sha256_hash(message : str) -> str:
        cipher = hashlib.sha256()
        cipher.update(message.encode())
        return cipher.hexdigest()
    

class RSACryptography:
    @staticmethod
    def key_generation(filename:str) -> None:
        public,private = rsa.newkeys(2048)
        root_filepath= "/vol/web/static/password_rsa/"
        file_path = root_filepath + filename
        with open(file_path + "/cryptography_file_for_server.public","wb") as f:
            f.write(public.save_pkcs1("PEM"))
        with open(file_path + "/cryptography_file_for_server.private","wb") as f:
            f.write(private.save_pkcs1("PEM"))

    @staticmethod
    def encryption(filename : str,message:bytes) -> bytes:
        root_filepath= "/vol/web/static/password_rsa/"
        file_path = root_filepath + filename
        with open(file_path + "/cryptography_file_for_server.public","rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        result = rsa.encrypt(message,public_key)
        return result

    @staticmethod
    def decryption(filename : str,cipher:bytes) -> bytes:
        root_filepath= "/vol/web/static/password_rsa/"
        file_path = root_filepath + filename
        with open(file_path + "/cryptography_file_for_server.private","rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        result = rsa.decrypt(cipher,private_key)
        return result

    @staticmethod
    def sign(message : bytes) -> bytes:
        with open("/vol/web/static/password_rsa/server/cryptography_file_for_server.private","rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        result = rsa.sign(message,private_key,"sha256")

    @staticmethod
    def verify_sign(message: bytes,signature:bytes) -> bytes:
        with open("/vol/web/static/password_rsa/server/cryptography_file_for_server.public","rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        try:
            rsa.verify(message,signature,public_key)
            return True
        except rsa.VerificationError:
            return False


class AESCryptography:
    @staticmethod
    def key_generation(password : str) -> bytes:
        salt = get_random_bytes(32)
        secret_key = PBKDF2(password,salt,dkLen=32)
        return secret_key

    @staticmethod
    def encryption(secret_key:bytes,message : bytes) -> bytes:
        cipher = AES.new(secret_key,AES.MODE_CBC)
        result = cipher.iv + cipher.encrypt(pad(message, AES.block_size))
        return result


    @staticmethod
    def decryption(message : bytes,secret_key:bytes) -> bytes:
        iv = message[16:]
        cipher_text = message[16:]
        cipher = AES.new(secret_key,AES.MODE_CBC,iv=iv)
        orginal = unpad(cipher.decrypt(cipher_text), AES.block_size)
        return orginal



if __name__ =='__main__':
    if not os.path.exists("/vol/web/static/password_rsa/server/"):
        RSACryptography.key_generation("server")