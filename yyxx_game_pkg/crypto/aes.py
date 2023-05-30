# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/03/28 10:44:11
# @Software : python3.11
# @Desc     : AES encryption AES 加密
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCrypto:
    def __init__(self, key: str, iv: str, block_size: int = AES.block_size):
        """
        :param key: AES 秘钥key
        :param iv: AES 密钥偏移量iv
        :param block_size:
        """
        self.key = key
        self.iv = iv if iv else key[:block_size]
        self.block_size = block_size
        self.cipher = AES.new(
            key=self.key.encode(), mode=AES.MODE_CBC, iv=self.iv.encode()
        )

    def encryption(self, data: str) -> str:
        """
        AES 加密
        """
        text = pad(data.encode(), self.block_size)
        encrypted = self.cipher.encrypt(text)
        return b64encode(encrypted).decode()

    def decryption(self, data: str) -> str:
        """
        AES 解密
        """
        encrypted = b64decode(data)
        decrypted = self.cipher.decrypt(encrypted)
        return unpad(decrypted, self.block_size).decode()
