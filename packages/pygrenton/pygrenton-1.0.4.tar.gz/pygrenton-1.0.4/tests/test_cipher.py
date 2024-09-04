
import pytest

from pygrenton.cipher import GrentonCipher

@pytest.fixture
def cipher() -> GrentonCipher:
    key = "RwHGl8yQVJmU8mc4s1KNKg=="
    iv = "Kv2bAZd7nJCsXUWCX+lbMA=="
    return GrentonCipher(key, iv)

def test_grenton_cipher_encrypt(cipher: GrentonCipher):
    encrypted_message = b'\xf8\xf5\xf8\xd5\xfc\xdb\x08O\xd1[\xa9\x99I\x1f\xa3^'
    assert cipher.encrypt("test_message".encode("utf-8")) == encrypted_message
    
def test_grenton_cipher_decrypt(cipher: GrentonCipher):
    encrypted_message = b'\xf8\xf5\xf8\xd5\xfc\xdb\x08O\xd1[\xa9\x99I\x1f\xa3^'
    assert cipher.decrypt(encrypted_message).decode("utf-8") == "test_message"