# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/20 20:02:59
# @Software : python3.11
# @Desc     : rsa
import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature


class RSACrypto:
    @staticmethod
    def generator_rsa(filename=None):
        random_generator = Random.new().read
        rsa = RSA.generate(1024, random_generator)
        rsa_private_key = rsa.exportKey()
        rsa_public_key = rsa.publickey().exportKey()

        if filename is not None:
            with open(f"{filename}_private.pem", "w") as f:
                f.write(rsa_private_key.decode())
            with open(f"{filename}_public.pem", "w") as f:
                f.write(rsa_public_key.decode())

    @staticmethod
    def rsa_public_crypto(raw_str: str, public_key: str) -> str:
        """
        公钥加密
        :param raw_str: raw string
        :param public_key: public key
        """
        cipher = PKCS1_cipher.new(RSA.importKey(public_key))
        encrypt_text = base64.b64encode(cipher.encrypt(raw_str.encode("utf-8")))
        return encrypt_text.decode("utf-8")

    @staticmethod
    def rsa_private_crypto(crypto_str: str, private_key: str) -> str:
        """
        私钥解密
        :param crypto_str: 加密字符串
        :param private_key: private key
        """
        cipher = PKCS1_cipher.new(RSA.importKey(private_key))
        decrypt_text = cipher.decrypt(base64.b64decode(crypto_str), Random.new().read)
        return decrypt_text.decode("utf-8")

    @staticmethod
    def rsa_private_sign(raw_str: str, private_key: str) -> str:
        """
        私钥签名
        :param raw_str: raw string
        :param private_key:
        """
        private_key = RSA.importKey(private_key)
        signer = PKCS1_signature.new(private_key)
        digest = SHA256.new()
        digest.update(raw_str.encode("utf8"))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        signature = signature.decode("utf-8")
        return signature

    @staticmethod
    def rsa_public_sign(raw_str: str, sign: str, public_key: str) -> bool:
        """
        公钥验证签名
        :param raw_str: raw string
        :param sign: 签名
        :param public_key: public key
        """
        public_key = RSA.importKey(public_key)
        verifier = PKCS1_signature.new(public_key)
        digest = SHA256.new()
        digest.update(raw_str.encode("utf-8"))
        return verifier.verify(digest, base64.b64decode(sign))
