#!/usr/bin/env python3
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProxyStyle, QStyle, QApplication, QDialog
from src.views.forms.landingForm import LandingForm
############################################################
# Main App                                                 #
############################################################
from src.models.AppFonts import RegularFont
from src.models.SessionWrapper import SessionWrapper

############################################################
# Create a custom "QProxyStyle" to enlarge the QMenu icons #
############################################################
from src.views.forms.loginForm import Login


class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
        if QStyle_PixelMetric == QStyle.PM_ToolBarIconSize:
            return 40
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


############################################################
# instantiate the app with login dialog                    #
############################################################

def run_app():
    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("Offline Docs")
    app.setWindowIcon(QIcon('resources/assets/images/logo.png'))
    app_font = RegularFont()
    app.setFont(app_font)
    myStyle = MyProxyStyle('Fusion')
    app.setStyle(myStyle)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    screen_center = screen.availableGeometry().center()
    # print('Available: %dx%d' % (rect.width(), rect.height()))
    SessionWrapper.screen_dim = ('%dx%d' % (rect.width(), rect.height()))
    SessionWrapper.screen_width = rect.width()
    SessionWrapper.screen_height = rect.height()
    # print('Screen: %s' % screen.name())
    # size = screen.size()
    # print('Size: %d x %d' % (size.width(), size.height()))

    css_file = "resources/assets/css/style.qss"
    app.setStyleSheet(open(css_file, "r").read())
    login = Login()
    ############################################################
    # if login succeed start the main page                     #
    ############################################################
    login_result = login.exec_()
    if login_result == QDialog.Accepted and login.status == "Done":
        window = LandingForm()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
