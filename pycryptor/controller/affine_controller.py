from ciphers.commons.alphabet import Alphabet
from ciphers.cipher.affine_cipher import AffineCipher
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.controller.base_controller import BaseController


class AffineController(BaseController):
    '''Controller that handles the Affine cipher's operations.
    '''
    
    def __init__(self) -> None:
        alphabet = Alphabet('es', ENGLISH_LOWERCASE, ENGLISH_UPPERCASE)
        super().__init__(alphabet, AffineCipher(alphabet=alphabet))