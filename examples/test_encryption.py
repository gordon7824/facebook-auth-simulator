#!/usr/bin/env python
"""示例：RSA 密码加密测试。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fb_simulator.crypto import RSAPasswordEncryptor


def main():
    print("RSA 密码加密演示\n")
    
    encryptor = RSAPasswordEncryptor(key_size=2048)
    private_pem, public_pem = encryptor.generate_keypair()
    
    print("公钥 (PEM):")
    print(public_pem[:100] + "...\n")
    
    password = "MySecurePassword123!"
    encrypted = encryptor.encrypt_password(password)
    
    print(f"原始密码: {password}")
    print(f"加密结果 (Base64): {encrypted[:50]}...\n")
    
    decrypted = encryptor.decrypt_password(encrypted)
    print(f"解密结果: {decrypted}")
    print(f"验证: {password == decrypted}")


if __name__ == "__main__":
    main()
