import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.commons.constants import DIALOG_OK_ICON
from pycryptor.commons.constants import DIALOG_CANCEL_ICON
from pycryptor.controller.caesar_controller import CaesarController
from pycryptor.gui.widgets.alphabet_form import AlphabetForm
from pycryptor.gui.widgets.cipher_text_form import CipherTextForm


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/CaesarView.glade')
class CaesarView(Gtk.Box):
    '''View that displays the Caesar Cipher.
    '''
    
    __slots__ = [
        '__app',
        '__cipher_controller',
        '__alphabet_form',
        '__is_shifts_good',
        '__cipher_text_form'
    ]
    __gtype_name__ = 'CaesarView'

    cipher_form_grid = Gtk.Template.Child()
    shifts_label = Gtk.Template.Child()
    shifts_spinbutton = Gtk.Template.Child()
    cipher_text_box = Gtk.Template.Child()
    actionbar = Gtk.Template.Child()

    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.app = application
        self.cipher_controller = CaesarController()
        self.is_shifts_good = False
        self.alphabet_form = AlphabetForm(self.app, self)
        self.cipher_text_form = CipherTextForm(self.app, self)
        # Display the alphabet form in the view
        self.cipher_form_grid.attach(
            self.alphabet_form.uppercase_alphabet_label, 0, 0, 1, 1
        )
        self.cipher_form_grid.attach(
            self.alphabet_form.uppercase_entry, 1, 0, 1, 1
        )
        self.cipher_form_grid.attach(
            self.alphabet_form.uppercase_error_revealer, 1, 1, 1, 1
        )
        self.cipher_form_grid.attach(
            self.alphabet_form.lowercase_alphabet_label, 0, 2, 1, 1
        )
        self.cipher_form_grid.attach(
            self.alphabet_form.lowercase_entry, 1, 2, 1, 1
        )
        self.cipher_form_grid.attach(
            self.alphabet_form.lowercase_error_revealer, 1, 3, 1, 1
        )
        # Add the cipher text form
        self.cipher_text_box.pack_start(self.cipher_text_form, True, True, 0)
        # Add cipher text form callbacks to alphabet form entries
        for entry in [
            self.alphabet_form.uppercase_entry,
            self.alphabet_form.lowercase_entry
        ]:
            for callback in [
                self.cipher_text_form.enable_disable_decryption_button,
                self.cipher_text_form.enable_disable_encryption_button
            ]:
                entry.connect(
                    'changed',
                    callback
                )
            # Add current view checking to alphabet form
            if entry in [
                self.alphabet_form.uppercase_entry,
                self.alphabet_form.lowercase_entry
            ]:
                entry.connect('changed', self.check_shifts_on_changed)

        # Add buttons to action bar
        self.actionbar.pack_start(self.cipher_text_form.encrypt_button)
        self.actionbar.pack_start(self.cipher_text_form.decrypt_button)
        # start initial state
        self.set_initial_state()

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def cipher_controller(self) -> CaesarController:
        return self.__cipher_controller

    @cipher_controller.setter
    def cipher_controller(self, cipher_controller: CaesarController) -> None:
        self.__cipher_controller = cipher_controller

    @property
    def is_alphabet_good(self) -> bool:
        return self.alphabet_form.is_alphabet_good

    @property
    def is_shifts_good(self) -> bool:
        return self.__is_shifts_good

    @is_shifts_good.setter
    def is_shifts_good(self, is_shifts_good: bool) -> None:
        self.__is_shifts_good = is_shifts_good

    @property
    def alphabet_form(self) -> Gtk.Box:
        return self.__alphabet_form

    @alphabet_form.setter
    def alphabet_form(self, alphabet_form: Gtk.Box) -> None:
        self.__alphabet_form = alphabet_form

    @property
    def cipher_text_form(self) -> Gtk.Box:
        return self.__cipher_text_form

    @cipher_text_form.setter
    def cipher_text_form(self, cipher_text_form: Gtk.Box) -> None:
        self.__cipher_text_form = cipher_text_form

    def set_initial_state(self) -> None:
        '''Sets the initial state for the window.
        '''
        self.shifts_spinbutton.set_value(
            self.cipher_controller.cipher.shift
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
            self.cipher_controller.cipher.shift = int(shifts)
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


