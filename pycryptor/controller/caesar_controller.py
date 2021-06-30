from ciphers.commons.alphabet import Alphabet
from ciphers.cipher.caesar_cipher import CaesarCipher
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.controller.base_controller import BaseController


class CaesarController(BaseController):
    '''Controller that handles the Caesar cipher's operations.
    '''
    
    def __init__(self) -> None:
        alphabet = Alphabet('es', ENGLISH_LOWERCASE, ENGLISH_UPPERCASE)
        super().__init__(alphabet, CaesarCipher(alphabet=alphabet))