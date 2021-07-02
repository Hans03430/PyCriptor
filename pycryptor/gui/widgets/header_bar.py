import gi

gi.require_version('Gtk', '3.0')

from gi.repository import GdkPixbuf
from gi.repository import Gtk
from pycryptor.commons.constants import DATA_DIRECTORY


@Gtk.Template(filename=f'{DATA_DIRECTORY}/ui/HeaderBar.glade')
class HeaderBar(Gtk.Box):
    '''Header bar of the PyCryptor application.
    '''
    
    __slots__ = ['__app', '__stack']
    __gtype_name__ = 'HeaderBar'

    left_headerbar = Gtk.Template.Child()
    right_headerbar = Gtk.Template.Child()
    left_headerbar_box = Gtk.Template.Child()
    pycryptor_menu_button = Gtk.Template.Child()
    menu_popover = Gtk.Template.Child()
    pycryptor_about_dialog = Gtk.Template.Child()

    def __init__(
        self,
        application: Gtk.Application,
        window: Gtk.ApplicationWindow
    ) -> None:
        super().__init__()
        self.app = application
        self.window = window
        self.left_headerbar_box.set_allocation(self.window.pycryptor_sidebar.get_allocation())
        # Set about dialog logo
        self.pycryptor_about_dialog.set_logo(
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                f'{DATA_DIRECTORY}/resources/icon.png',
                64, 64
            )
        )

    @property
    def app(self) -> Gtk.Application:
        return self.__app

    @app.setter
    def app(self, app: Gtk.Application) -> None:
        self.__app = app

    @Gtk.Template.Callback()
    def show_about_dialog(self, widget: Gtk.Button) -> None:
        '''Shows the About PyCryptor dialog.
        '''
        self.pycryptor_about_dialog.show_all()