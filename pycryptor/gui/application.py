import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.gui.main_window import MainWindow


class Application(Gtk.Application):
    '''Application that holds PyCryptor.
    '''
    
    __slots__ = ['__window']

    pycryptor_application_window = Gtk.Template.Child('MainWindow')

    def __init__(self, application_id: str) -> None:
        super().__init__(application_id=application_id)
        self.window = None

    def do_activate(self) -> None:
        if not self.window: # No window available
            self.window = MainWindow(self, 'PyCryptor')
            self.window.show_all()

    @property
    def window(self) -> MainWindow:
        return self.__window

    @window.setter
    def window(self, window: MainWindow) -> None:
        self.__window = window


