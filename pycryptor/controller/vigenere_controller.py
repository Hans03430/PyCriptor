from ciphers.commons.alphabet import Alphabet
from ciphers.cipher.vigenere_cipher import VigenereCipher
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.controller.base_controller import BaseController


class VigenereController(BaseController):
    '''Controller that handles the Vigenere cipher's operations.
    '''
    
    def __init__(self) -> None:
        alphabet = Alphabet('es', ENGLISH_LOWERCASE, ENGLISH_UPPERCASE)
        super().__init__(alphabet, VigenereCipher(alphabet=alphabet))