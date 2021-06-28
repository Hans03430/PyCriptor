import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/HeaderBar.glade')
class CaesarView(Gtk.Box):
    '''View that displays the Caesar Cipher.
    '''
    
    __slots__ = ['__app']
    __gtype_name__ = 'CaesarView'

    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.app = application

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app
