
import sys
import pywebio

from views import mainView

def main():
    mainView.view()

try:
    port=8089
    pywebio.start_server(main, port=port, debug=True)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    mainView.clean_up()
    sys.exit(0)
