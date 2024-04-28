from authentication.models import UserProfile
from django.contrib.auth.models import User
from note.models import FileModel
from secure_note.user_defined import cryptoengine
import random


class Recover:
    @staticmethod
    def regenerateAESKey(user: User,userprofile:UserProfile) -> UserProfile:
        random_value = str(random.randbytes(10))
        aes_key = cryptoengine.AESCryptography.key_generation(random_value)
        if userprofile.previous_hashed_password is not None:
            Recover.reGenerateRSAKey(user,userprofile)
        userprofile = Recover.reEncryptFile(user,userprofile,aes_key)
        return userprofile

    @staticmethod
    def reGenerateRSAKey(user:User,userprofile:UserProfile) -> None:
        file_path = userprofile.file_path
        aes_key = cryptoengine.RSACryptography.decryption(file_path,userprofile.hashed_password)
        cryptoengine.RSACryptography.key_generation(file_path)
        userprofile.previous_hashed_password = userprofile.hashed_password
        userprofile.hashed_password = cryptoengine.RSACryptography.encryption(file_path,aes_key)
        userprofile.signed_password = cryptoengine.RSACryptography.sign(userprofile.hashed_password)
        userprofile.save()

    @staticmethod
    def reEncryptFile(user:User,userprofile:UserProfile,aes_key:bytes) -> UserProfile:
        file_list = FileModel.objects.filter(user=user)
        aes_old_key = cryptoengine.RSACryptography.decryption(userprofile.file_path, userprofile.hashed_password)
        for i in file_list:
            file_content = cryptoengine.AESCryptography.decryption(i.content,aes_old_key)
            i.content = cryptoengine.AESCryptography.encryption(aes_key,file_content)
            i.save()
        userprofile.previous_hashed_password = userprofile.hashed_password
        userprofile.hashed_password = cryptoengine.RSACryptography.encryption(userprofile.file_path,aes_key)
        userprofile.signed_password = cryptoengine.RSACryptography.sign(aes_key)
        userprofile.save()
        return userprofile