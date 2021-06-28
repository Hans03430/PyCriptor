import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/HeaderBar.glade')
class HeaderBar(Gtk.HeaderBar):
    '''Header bar of the PyCryptor application.
    '''
    
    __slots__ = ['__app', '__stack']
    __gtype_name__ = 'HeaderBar'

    pycryptor_stack_switcher = Gtk.Template.Child()

    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.app = application
        self.stack = Gtk.Stack()
        # Add views to the stack
        self.stack.add_titled(Gtk.Label(), 'Caesar', 'Caesar')
        self.stack.add_titled(Gtk.Button(), 'Affine', 'Affine')
        self.stack.add_titled(Gtk.Label(), 'Atbash', 'Atbash')
        self.stack.add_titled(Gtk.Label(), 'Vigenère', 'Vigenère')
        # Add stack to switcher
        self.pycryptor_stack_switcher.set_stack(self.stack)

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def stack(self) -> Gtk.Stack:
        return self.__stack

    @stack.setter
    def stack(self, stack: Gtk.Stack) -> None:
        self.__stack = stack
