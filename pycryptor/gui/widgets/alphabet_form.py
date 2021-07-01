import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.commons.constants import DIALOG_OK_ICON
from pycryptor.commons.constants import DIALOG_CANCEL_ICON
from pycryptor.commons.constants import ENGLISH_LOWERCASE
from pycryptor.commons.constants import ENGLISH_UPPERCASE
from pycryptor.controller.base_controller import BaseController


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/AlphabetForm.glade')
class AlphabetForm(Gtk.Box):
    '''Widgets that make up the Alphabet form.
    '''
    
    __slots__ = [
        '__app',
        '__cipher_view',
        '__is_alphabet_good',
    ]
    __gtype_name__ = 'AlphabetForm'

    uppercase_alphabet_label = Gtk.Template.Child()
    lowercase_alphabet_label = Gtk.Template.Child()
    uppercase_entry = Gtk.Template.Child()
    lowercase_entry = Gtk.Template.Child()
    uppercase_error_revealer = Gtk.Template.Child()
    lowercase_error_revealer = Gtk.Template.Child()
    uppercase_error_label = Gtk.Template.Child()
    lowercase_error_label = Gtk.Template.Child()

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
        self.is_alphabet_good = False
        self.set_initial_state()

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def cipher_controller(self) -> BaseController:
        return self.cipher_view.cipher_controller

    @property
    def is_alphabet_good(self) -> bool:
        return self.__is_alphabet_good

    @is_alphabet_good.setter
    def is_alphabet_good(self, is_alphabet_good: bool) -> None:
        self.__is_alphabet_good = is_alphabet_good

    def set_initial_state(self) -> None:
        '''Sets the initial state for the form.
        '''
        self.uppercase_entry.set_text(ENGLISH_UPPERCASE)
        self.lowercase_entry.set_text(ENGLISH_LOWERCASE)

    @Gtk.Template.Callback()
    def check_alphabet_on_changed(self, widget: Gtk.Entry) -> None:
        '''Check if the alphabet is ok or not. Shows feedback and updates the
        alphabet for the Cipher object.
        '''
        # Check alphabet
        try:
            self.cipher_controller.add_new_alphabet(
                lower=self.lowercase_entry.get_text(),
                upper=self.uppercase_entry.get_text()
            )
            self.is_alphabet_good = True
        except AttributeError as ae:
            self.is_alphabet_good = False
            # Update erorr message
            for label in [
                self.uppercase_error_label,
                self.lowercase_error_label
            ]:
                label.set_text(str(ae))
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
