"""加密工具（本地测试用）。"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
from typing import Tuple


class RSAPasswordEncryptor:
    """RSA 密码加密器（本地测试用）。"""
    
    def __init__(self, key_size: int = 2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
    
    def generate_keypair(self) -> Tuple[str, str]:
        """生成 RSA 密钥对。"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        return private_pem, public_pem
    
    def load_public_key_pem(self, pem: str):
        """加载 PEM 格式的公钥。"""
        self.public_key = serialization.load_pem_public_key(
            pem.encode('utf-8'),
            backend=default_backend()
        )
    
    def encrypt_password(self, password: str) -> str:
        """加密密码（返回 Base64）。"""
        if not self.public_key:
            raise ValueError("Public key not loaded")
        
        encrypted = self.public_key.encrypt(
            password.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_password(self, encrypted_b64: str) -> str:
        """解密密码。"""
        if not self.private_key:
            raise ValueError("Private key not loaded")
        
        encrypted = base64.b64decode(encrypted_b64)
        decrypted = self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')
