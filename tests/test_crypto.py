"""测试加密功能。"""

import pytest
from src.fb_simulator.crypto import RSAPasswordEncryptor


def test_rsa_encrypt_decrypt():
    """测试 RSA 加密解密。"""
    encryptor = RSAPasswordEncryptor(key_size=2048)
    encryptor.generate_keypair()
    
    password = "TestPassword123!"
    encrypted = encryptor.encrypt_password(password)
    decrypted = encryptor.decrypt_password(encrypted)
    
    assert decrypted == password
