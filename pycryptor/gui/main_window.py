import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY
from pycryptor.gui.widgets.header_bar import HeaderBar


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/MainWindow.glade')
class MainWindow(Gtk.ApplicationWindow):
    '''Main window where PyCryptor runs.
    '''
    
    __slots__ = ['__app', '__header_bar']
    __gtype_name__ = 'MainWindow'

    pycryptor_application_window = Gtk.Template.Child('MainWindow')

    def __init__(self, application: Gtk.Application, title: str) -> None:
        super().__init__(application=application, title=title)
        self.app = application
        # Add header bar
        self.header_bar = HeaderBar(self.app)
        self.set_titlebar(self.header_bar)
        self.add(self.header_bar.stack)
        self.maximize()

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @property
    def header_bar(self) -> Gtk.HeaderBar:
        return self.__header_bar

    @header_bar.setter
    def header_bar(self, header_bar: Gtk.HeaderBar) -> None:
        self.__header_bar = header_bar

