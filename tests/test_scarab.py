"""Scarab wrapper unit tests"""

from scarab import generate_pair, PublicKey, PrivateKey, EncryptedArray

from loader import ScarabLoader
from typedefs import c_mpz_t, c_fhe_sk_t, c_fhe_pk_t

from nose.tools import *


load_scarab = ScarabLoader()
scarab = load_scarab()


class TestTypedefs(object):

    """Test typedefs"""

    def test_sk_init(self):
        sk = c_fhe_sk_t()
        scarab.fhe_sk_init(sk)

    def test_pk_init(self):
        pk = c_fhe_pk_t()
        scarab.fhe_pk_init(pk)


class TestEncryptedArray(object):

    """EncryptedArray unit tests"""

    def setup(self):
        self.array = EncryptedArray(16)

    def test_iteration(self):
        counter = 0
        for c in self.array:
            counter += 1
            assert_not_equals(c, None)
        assert_equals(counter, 16)

    def test_get(self):
        self.array[5]
        assert_raises(Exception, self.array, 16)

    def test_set(self):
        self.array[5] = None
        assert_equals(self.array[5], None)

    def test_len(self):
        assert_equals(len(self.array), 16)


class TestEncryption(object):

    """Test key generation and encryption"""

    def setup(self):
        self.pk, self.sk = generate_pair()

    def test_generate_pair(self):
        assert_not_equals(self.pk.raw, 0)
        assert_not_equals(self.sk.raw, 0)

    def test_encryption(self):
        m = [1, 0, 1, 0, 1, 0, 1, 0]
        c = self.pk.encrypt(m)
        p = self.sk.decrypt(c)
        assert_equals(m, p)