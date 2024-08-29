import unittest
from unittest.mock import patch, MagicMock
import base64

import streamlit as st
import sys

st.cache_data.clear()
st.cache_resource.clear()

mock_components = MagicMock()
patch('streamlit.components.v1.components', mock_components).start()

from streamlit_cookies_manager.encrypted_cookie_manager import key_from_parameters, EncryptedCookieManager

class TestEncryptedCookieManager(unittest.TestCase):

    def test_key_from_parameters(self):
        salt = b'test_salt'
        iterations = 100000
        password = 'test_password'

        key = key_from_parameters(salt, iterations, password)

        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), 44)  # Base64 encoded 32-byte key

    def test_encrypted_cookie_manager_initialization(self):
        with patch('streamlit_cookies_manager.encrypted_cookie_manager.CookieManager') as mock_cookie_manager:
            mock_cookie_manager.return_value = MagicMock()
            
            ecm = EncryptedCookieManager(password='test_password')
            
            self.assertIsNotNone(ecm)
            self.assertIsNone(ecm._fernet)
            mock_cookie_manager.assert_called_once_with(path=None, prefix='')

    def test_encrypted_cookie_manager_set_get(self):
        with patch('streamlit_cookies_manager.encrypted_cookie_manager.CookieManager') as mock_cookie_manager, \
             patch('streamlit_cookies_manager.encrypted_cookie_manager.Fernet') as mock_fernet:
            mock_cookie_manager.return_value = MagicMock()
            mock_fernet.return_value = MagicMock()
            mock_fernet.return_value.encrypt.return_value = b'encrypted_value'
            mock_fernet.return_value.decrypt.return_value = b'decrypted_value'
            
            ecm = EncryptedCookieManager(password='test_password')
            ecm._fernet = mock_fernet.return_value  # Set up the Fernet mock
            
            ecm['test_key'] = 'test_value'
            self.assertEqual(ecm['test_key'], 'decrypted_value')

if __name__ == '__main__':
    unittest.main()