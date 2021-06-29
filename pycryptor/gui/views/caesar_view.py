import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.commons.texts import DECRYPT_STR
from pycryptor.commons.texts import ENCRYPT_STR
from ciphers.commons.alphabet import Alphabet


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/CaesarView.glade')
class CaesarView(Gtk.Box):
    '''View that displays the Caesar Cipher.
    '''
    
    __slots__ = ['__app', '__alphabet']
    __gtype_name__ = 'CaesarView'

    uppercase_entry = Gtk.Template.Child()
    lowercase_entry = Gtk.Template.Child()
    shifts_spinbutton = Gtk.Template.Child()
    plain_entry = Gtk.Template.Child()
    ciphered_entry = Gtk.Template.Child()
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

    def set_initial_state(self) -> None:
        '''Sets the initial state for the window.
        '''
        self.alphabet = None
        self.uppercase_entry.set_text(ENGLISH_UPPERCASE)
        self.lowercase_entry.set_text(ENGLISH_LOWERCASE)

        self.check_alphabet_on_changed(self.lowercase_entry)

    @Gtk.Template.Callback()
    def check_alphabet_on_changed(self, widget: Gtk.Button) -> None:
        '''Check if the alphabet is ok or not. Shows feedback.
        '''
        if self.is_alphabet_correct():
            icon_name = 'dialog-ok'
            self.lowercase_error_revealer.set_reveal_child(False)
            self.uppercase_error_revealer.set_reveal_child(False)
        else:
            icon_name = None
            self.lowercase_error_revealer.set_reveal_child(True)
            self.uppercase_error_revealer.set_reveal_child(True)

        # Set icon if it's ok
        self.uppercase_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY,
            icon_name
        )
        self.lowercase_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY,
            icon_name
        )

    def is_alphabet_correct(self) -> bool:
        '''Method that checks if the alphabets have the same length.
        
        Returns
        -------
        response: bool
            True if correct, else false.
        '''
        uppercase_alphabet = self.uppercase_entry.get_text()
        lowercase_alphabet = self.lowercase_entry.get_text()

        try:
            self.alphabet = Alphabet(
                lower=lowercase_alphabet,
                upper=uppercase_alphabet
            )
            return True
        except AttributeError as ae:
            return False

