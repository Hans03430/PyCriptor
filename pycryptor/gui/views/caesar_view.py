import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.commons.constants import DIALOG_OK_ICON
from pycryptor.commons.constants import DIALOG_CANCEL_ICON
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.commons.texts import DECRYPT_STR
from pycryptor.commons.texts import ENCRYPT_STR
from pycryptor.controller.caesar_controller import CaesarController
from ciphers.commons.alphabet import Alphabet


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/CaesarView.glade')
class CaesarView(Gtk.Box):
    '''View that displays the Caesar Cipher.
    '''
    
    __slots__ = [
        '__app',
        '__caesar_controller',
        '__is_alphabet_good',
        '__is_shifts_good'
    ]
    __gtype_name__ = 'CaesarView'

    uppercase_entry = Gtk.Template.Child()
    lowercase_entry = Gtk.Template.Child()
    shifts_spinbutton = Gtk.Template.Child()
    plain_text_buffer = Gtk.Template.Child()
    ciphered_text_buffer= Gtk.Template.Child()
    caesar_actionbar = Gtk.Template.Child()
    uppercase_error_revealer = Gtk.Template.Child()
    lowercase_error_revealer = Gtk.Template.Child()

    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.app = application
        # Action bar buttons
        self.encrypt_button = Gtk.Button.new_with_label(ENCRYPT_STR)
        self.decrypt_button = Gtk.Button.new_with_label(DECRYPT_STR)
        self.caesar_actionbar.pack_start(self.encrypt_button)
        self.caesar_actionbar.pack_start(self.decrypt_button)
        self.caesar_controller = CaesarController()
        # Add callbacks to encrypt/decrypt button
        self.encrypt_button.connect('clicked', self.encrypt_text)
        self.decrypt_button.connect('clicked', self.decrypt_text)
        self.set_initial_state()

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def alphabet(self) -> Alphabet:
        return self.__alphabet

    @alphabet.setter
    def alphabet(self, alphabet: Alphabet) -> None:
        self.__alphabet = alphabet

    @property
    def caesar_controller(self) -> CaesarController:
        return self.__caesar_controller

    @caesar_controller.setter
    def caesar_controller(self, caesar_controller: CaesarController) -> None:
        self.__caesar_controller = caesar_controller

    @property
    def is_alphabet_good(self) -> bool:
        return self.__is_alphabet_good

    @is_alphabet_good.setter
    def is_alphabet_good(self, is_alphabet_good: bool) -> None:
        self.__is_alphabet_good = is_alphabet_good

    @property
    def is_shifts_good(self) -> bool:
        return self.__is_shifts_good

    @is_alphabet_good.setter
    def is_shifts_good(self, is_shifts_good: bool) -> None:
        self.__is_shifts_good = is_shifts_good

    def set_initial_state(self) -> None:
        '''Sets the initial state for the window.
        '''
        self.uppercase_entry.set_text(ENGLISH_UPPERCASE)
        self.lowercase_entry.set_text(ENGLISH_LOWERCASE)
        self.shifts_spinbutton.set_value(
            self.caesar_controller.cipher.shift
        )

    @Gtk.Template.Callback()
    def check_alphabet_on_changed(self, widget: Gtk.Entry) -> None:
        '''Check if the alphabet is ok or not. Shows feedback and updates the
        alphabet for the Cipher object.
        '''
        # Check alphabet
        try:
            self.caesar_controller.add_new_alphabet(
                lower=self.lowercase_entry.get_text(),
                upper=self.uppercase_entry.get_text()
            )
            self.is_alphabet_good = True
        except AttributeError as ae:
            self.is_alphabet_good = False
        # Update visual feedback
        if self.is_alphabet_good:
            icon_name = DIALOG_OK_ICON
            self.lowercase_error_revealer.set_reveal_child(False)
            self.uppercase_error_revealer.set_reveal_child(False)
        else:
            icon_name = DIALOG_CANCEL_ICON
            self.lowercase_error_revealer.set_reveal_child(True)
            self.uppercase_error_revealer.set_reveal_child(True)

        # Set icon if it's ok
        for entry in [self.uppercase_entry, self.lowercase_entry]:
            entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY,
                icon_name
            )

    @Gtk.Template.Callback()
    def check_shifts_on_changed(self, widget: Gtk.Entry) -> None:
        '''Method that checks if the shifts for the Caesar cipher are ok or
        not. It also updates the shifts for the Cipher object.
        '''
        shifts = self.shifts_spinbutton.get_value()
        # check if type is float
        if type(shifts) == float:
            self.is_shifts_good = True
            self.caesar_controller.cipher.shift = int(shifts)
            icon_name = DIALOG_OK_ICON
        else: # Wrong type
            self.is_shifts_good = False
            icon_name = DIALOG_CANCEL_ICON
        # Update visual feedback
        self.shifts_spinbutton.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY,
            icon_name
        )

    def is_cipher_form_correct(self) -> bool:
        '''Method that checks whether the alphabet and the cipher's parameters
        are ok or not.
        '''
        return self.is_alphabet_good and self.is_shifts_good

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
        plain_text = self.plain_text_buffer.get_text(
            self.plain_text_buffer.get_start_iter(),
            self.plain_text_buffer.get_end_iter(),
            True
        )

        return self.is_cipher_form_correct() and len(plain_text) > 0

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
        ciphered_text = self.ciphered_text_buffer.get_text(
            self.ciphered_text_buffer.get_start_iter(),
            self.ciphered_text_buffer.get_end_iter(),
            True
        )

        return self.is_cipher_form_correct() and len(ciphered_text) > 0

    def encrypt_text(self, widget: Gtk.Button) -> None:
        '''Callback that starts the encryption of a the plain text.
        '''
        plain_text = self.plain_text_buffer.get_text(
            self.plain_text_buffer.get_start_iter(),
            self.plain_text_buffer.get_end_iter(),
            True
        )

        ciphered_text = self.caesar_controller.encrypt(plain_text)
        self.ciphered_text_buffer.set_text(ciphered_text)

    def decrypt_text(self, widget: Gtk.Button) -> None:
        '''Callback that starts the decryption of a the plain text.
        '''
        ciphered_text = self.ciphered_text_buffer.get_text(
            self.ciphered_text_buffer.get_start_iter(),
            self.ciphered_text_buffer.get_end_iter(),
            True
        )

        plain_text = self.caesar_controller.decrypt(ciphered_text)
        self.plain_text_buffer.set_text(plain_text)


