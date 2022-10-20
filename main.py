from AirControl import *
import sys

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    Application = AirControl()
    Application.show()
    sys.exit(app.exec_())
