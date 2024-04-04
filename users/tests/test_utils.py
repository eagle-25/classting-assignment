from common import settings
from users.utils import decrypt_aes, encrypt_aes


def test_encrypt_aes():
    """
    AES 암호화가 정상적으로 동작하는지 테스트한다.
    """
    # given
    data = "hello"
    key = settings.AES_KEY
    iv = settings.AES_IV
    # when
    res = encrypt_aes(data, key, iv)
    # then
    assert res != data


def test_decrypt_aes():
    """
    AES 복호화가 정상적으로 동작하는지 테스트한다.
    """
    # given
    data = "hello"
    key = settings.AES_KEY
    iv = settings.AES_IV
    encrypted_data = encrypt_aes(data, key, iv)
    # when
    res = decrypt_aes(encrypted_data, key, iv)
    # then
    assert res == data
