from ciphers.commons.alphabet import Alphabet
from ciphers.cipher.atbash_cipher import AtbashCipher
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.controller.base_controller import BaseController


class AtbashController(BaseController):
    '''Controller that handles the Atbash cipher's operations.
    '''
    
    def __init__(self) -> None:
        alphabet = Alphabet('es', ENGLISH_LOWERCASE, ENGLISH_UPPERCASE)
        super().__init__(alphabet, AtbashCipher(alphabet=alphabet))