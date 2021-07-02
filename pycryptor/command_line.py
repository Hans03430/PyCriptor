import sys

from pycryptor.gui.application import Application

def main() -> None:
    app = Application('PyCryptor')
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
