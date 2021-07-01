import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.commons.constants import DIALOG_OK_ICON
from pycryptor.commons.constants import DIALOG_CANCEL_ICON
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from ciphers.cipher.base_cipher import BaseCipher


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/CipherTextForm.glade')
class CipherTextForm(Gtk.Box):
    '''Widgets that make up the plain/encrypted text form.
    '''
    
    __slots__ = [
        '__app',
        '__cipher_view'
    ]
    __gtype_name__ = 'CipherTextForm'

    plain_label = Gtk.Template.Child()
    plain_text_view = Gtk.Template.Child()
    ciphered_label = Gtk.Template.Child()
    ciphered_text_view = Gtk.Template.Child()
    plain_buffer = Gtk.Template.Child()
    ciphered_buffer = Gtk.Template.Child()
    encrypt_button = Gtk.Template.Child()
    decrypt_button = Gtk.Template.Child()

    def __init__(
        self,
        application:
        Gtk.Application,
        cipher_view: Gtk.Box
    ) -> None:
        super().__init__()
        self.app = application
        # View that owns this form
        self.cipher_view = cipher_view
        self.set_initial_state()

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def cipher_controller(self) -> BaseCipher:
        return self.cipher_view.cipher_controller

    @property
    def is_alphabet_good(self) -> bool:
        return self.__is_alphabet_good

    @is_alphabet_good.setter
    def is_alphabet_good(self, is_alphabet_good: bool) -> None:
        self.__is_alphabet_good = is_alphabet_good

    @property
    def is_cipher_form_correct(self) -> bool:
        return self.cipher_view.is_cipher_form_correct()

    def set_initial_state(self) -> None:
        '''Sets the initial state for the form.
        '''
        self.plain_buffer.set_text('')
        self.ciphered_buffer.set_text('')

        for button in [self.encrypt_button, self.decrypt_button]:
            button.set_sensitive(False)
    
    @Gtk.Template.Callback()
    def enable_disable_encryption_button(self, widget: Gtk.Entry) -> None:
        '''Callback that checks whether to enable or disable the encryption
        button. Enable if there's text to encrypt and the form is correct.
        '''
        # Check if form is right and there's text to encrypt
        if self.is_encryption_good():
            self.encrypt_button.set_sensitive(True)
        else:
            self.encrypt_button.set_sensitive(False)

    def is_encryption_good(self) -> bool:
        '''Method that checks if everything is ok to encrypt a text or not.
        '''
        plain_text = self.plain_buffer.get_text(
            self.plain_buffer.get_start_iter(),
            self.plain_buffer.get_end_iter(),
            True
        )

        return self.is_cipher_form_correct and len(plain_text) > 0

    @Gtk.Template.Callback()
    def enable_disable_decryption_button(self, widget: Gtk.Entry) -> None:
        '''Callback that checks whether to enable or disable the decryption
        button. Enable if there's text to decrypt and the form is correct.
        '''
        # Check if form is right and there's text to encrypt
        if self.is_decryption_good():
            self.decrypt_button.set_sensitive(True)
        else:
            self.decrypt_button.set_sensitive(False)

    def is_decryption_good(self) -> bool:
        '''Method that checks if everything is ok to encrypt a text or not.
        '''
        ciphered_text = self.ciphered_buffer.get_text(
            self.ciphered_buffer.get_start_iter(),
            self.ciphered_buffer.get_end_iter(),
            True
        )
        return self.is_cipher_form_correct and len(ciphered_text) > 0

    @Gtk.Template.Callback()
    def encrypt_text(self, widget: Gtk.Button) -> None:
        '''Callback that starts the encryption of a the plain text.
        '''
        plain_text = self.plain_buffer.get_text(
            self.plain_buffer.get_start_iter(),
            self.plain_buffer.get_end_iter(),
            True
        )

        ciphered_text = self.cipher_controller.encrypt(plain_text)
        self.ciphered_buffer.set_text(ciphered_text)

    @Gtk.Template.Callback()
    def decrypt_text(self, widget: Gtk.Button) -> None:
        '''Callback that starts the decryption of a the plain text.
        '''
        ciphered_text = self.ciphered_buffer.get_text(
            self.ciphered_buffer.get_start_iter(),
            self.ciphered_buffer.get_end_iter(),
            True
        )

        plain_text = self.cipher_controller.decrypt(ciphered_text)
        self.plain_buffer.set_text(plain_text)
