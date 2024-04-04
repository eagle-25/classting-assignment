from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_aes(data: str, key: str, iv: str) -> str:
    data: bytes = data.encode("utf-8")
    key: bytes = key.encode("utf-8")
    iv: bytes = iv.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data).hex()


def decrypt_aes(data: str, key: str, iv: str) -> str:
    data: bytes = bytes.fromhex(data)
    key: bytes = key.encode("utf-8")
    iv: bytes = iv.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    return unpad(decrypted_data, AES.block_size).decode()
