from abc import ABC
from abc import abstractmethod
from ciphers.cipher.base_cipher import BaseCipher
from ciphers.commons.alphabet import Alphabet


class BaseController(ABC):
    '''Base class to define a controller.
    
    Attributes
    ----------
    __alphabet: Alphabet
        Current Alphabet the controller handles.
        
    __cipher: BaseCipher
        Current cipher used by the controller.
    '''

    __slots__ = ['__alphabet', '__cipher']

    def __init__(
        self,
        alphabet: Alphabet=None,
        cipher: BaseCipher=None
    ) -> None:
        self.alphabet = alphabet
        self.cipher = cipher

    @property
    def alphabet(self) -> Alphabet:
        return self.__alphabet

    @alphabet.setter
    def alphabet(self, alphabet: Alphabet) -> None:
        self.__alphabet = alphabet

    @property
    def cipher(self) -> Alphabet:
        return self.__cipher

    @cipher.setter
    def cipher(self, cipher: BaseCipher) -> None:
        self.__cipher = cipher
        # Assign current alphabet by default
        if self.alphabet:
            self.__cipher.alphabet = self.alphabet

    def add_new_alphabet(
        self,
        language: str='',
        lower: str='',
        upper: str=''
    ) -> None:
        '''Method that adds a new alphabet to the controller.

        Parameters
        ----------
        lower: str
            String that contains the lowercase letters in the alphabet.

        upper: str
            String that contains the uppercase letters in the alphabet.

        language: str
            Name of the language the alphabet belongs to.
        '''
        try:
            new_alphabet = Alphabet(language=language, lower=lower, upper=upper)
            self.alphabet = new_alphabet
            self.cipher.alphabet = self.alphabet
        except Exception as e:
            raise e

    def encrypt(self, text: str) -> str:
        '''Method that encrypts the given text.
        
        Paramters
        ---------
        text: str
            The text to encrypt.
            
        Returns
        -------
        encrypted: str
            Encrypted text.
        '''
        return self.cipher.encrypt(text)

    def decrypt(self, text: str) -> str:
        '''Method that decrypts the given text.
        
        Paramters
        ---------
        text: str
            The text to decrypt.
            
        Returns
        -------
        decrypted: str
            Decrypted text.
        '''
        return self.cipher.decrypt(text)
