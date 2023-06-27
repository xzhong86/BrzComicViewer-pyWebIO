
import pywebio

from views import mainView

def main():
    mainView.view()

port=8089
pywebio.start_server(main, port=port, debug=True)
