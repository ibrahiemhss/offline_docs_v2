from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QHBoxLayout, QWidget, QVBoxLayout
from src.viewModels.login import LoginModel
from src.views.widgets.ClickableLabel import ForgotPasswordLabel, ClickableLabel
from src.views.widgets.CustomLabel import RegularLabel, HeadLineLabel
from src.views.widgets.MyCheckBox import CheckBox
from src.views.modals.createAccountModal import CreateAccountModal
from src.models.AppFonts import RegularFont
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.views.widgets.MessageBoxes import MessageBoxes


class Login(QDialog):
    def __init__(self):
        super().__init__()
        window_width = SessionWrapper.get_dimension('login_width')
        window_height = SessionWrapper.get_dimension('login_height')
        app_font = RegularFont()
        self.setFont(app_font)
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("login")
        self.status = "Not Done"
        self.initUI()

    def initUI(self):
        welcomeLabel = HeadLineLabel('Welcome !')
        welcomeLabel.setObjectName("welcome_label")
        welcomeLabel.setStyleSheet('welcome_label')
        # welcomeLabel.setAlignment(Qt.AlignCenter)
        userNameLabel = RegularLabel('Email :')
        # userNameLabel.setFixedWidth(100)
        userNameLabel.setObjectName("user_name_label")
        passWordLabel = RegularLabel('Password :')
        # passWordLabel.setFixedWidth(100)
        passWordLabel.setObjectName("pwd_label")
        self.userNameEdit = QLineEdit()
        self.userNameEdit.setObjectName("user_name_input")
        self.userNameEdit.setFixedWidth(250)
        self.passWordEdit = QLineEdit()
        self.passWordEdit.setObjectName("pwd_input")
        self.passWordEdit.setFixedWidth(250)
        self.passWordEdit.setEchoMode(QLineEdit.Password)
        self.passWordEdit.returnPressed.connect(lambda: self.handleLogin(self.userNameEdit.text(), self.passWordEdit.text()))

        self.column = QVBoxLayout()

        self.column.setContentsMargins(250, 100, 0, 50)  # (left, top, right, bottom)

        just_widget = QWidget()

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setColumnStretch(2, 5)  # column strech

        # grid.addWidget(welcomeLabel, 1, 0)

        grid.addWidget(userNameLabel, 1, 0)  # ( row, column)
        grid.addWidget(self.userNameEdit, 1, 1)

        grid.addWidget(passWordLabel, 2, 0)
        grid.addWidget(self.passWordEdit, 2, 1)

        btn_line = QHBoxLayout()

        btn_line.setContentsMargins(60, 20, 250, 20)
        btn_line.setSpacing(40)
        # self.buttonLogin = ClickableIcon(150, 40, "resources/assets/images/Login/login-button.png")
        self.buttonLogin = ClickableLabel("Login", bg_color="#CC1417")
        self.buttonLogin.setObjectName("buttonLogin")
        self.buttonLogin.setFixedWidth(150)
        self.buttonLogin.setAlignment(Qt.AlignCenter)
        self.buttonLogin.clicked.connect(lambda: self.handleLogin(self.userNameEdit.text(), self.passWordEdit.text()))

        # self.buttonRegister = ClickableIcon(150, 40, "resources/assets/images/Login/register-button.png")
        self.buttonRegister = ClickableLabel("Register", bg_color="#CC1417")

        self.buttonRegister.setObjectName("buttonRegister")
        self.buttonRegister.setFixedWidth(150)
        self.buttonRegister.setAlignment(Qt.AlignCenter)
        self.buttonRegister.clicked.connect(self.create_account)

        btn_line.addWidget(self.buttonLogin)
        btn_line.addWidget(self.buttonRegister)

        self.remember_me = self.remember_me_widget()
        sign_up_section = QHBoxLayout()
        sign_up_section.setSpacing(80)
        sign_up_section.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)
        forgot_label = ForgotPasswordLabel('<a href="#" style="color: #000">Forgot Password</a>')
        forgot_label.clicked.connect(self.create_account)
        sign_up_section.addWidget(self.remember_me)
        sign_up_section.addWidget(forgot_label)
        sign_up_Q = QWidget()
        sign_up_Q.setFixedHeight(60)
        sign_up_Q.setLayout(sign_up_section)
        just_widget.setLayout(grid)

        self.column.addWidget(welcomeLabel)
        self.column.addWidget(just_widget)
        self.column.addWidget(sign_up_Q)
        self.column.addLayout(btn_line)
        # self.resize(502, 261)
        self.setFixedSize(800, 500)
        self.setWindowTitle("Offline Docs / Sign In")
        self.setLayout(self.column)

    def handleLogin(self, email, password):
            remember_me = self.remember_me.checkState() == Qt.Checked
            login_try, msg = LoginModel.handleLogin(email, password, remember_me)
            if login_try == "Okay" and msg == "Done":
                self.status = "Done"
                self.accept()
            elif login_try == "Okay" and msg == "new":
                self.status = "New"
                self.accept()
            else:
                MessageBoxes.warning_message(login_try, msg)

    def create_account(self):
        reg_modal = CreateAccountModal()
        reg_modal_run = reg_modal.exec_()
        if reg_modal_run == QDialog.Accepted and reg_modal.result == "Done":
            self.userNameEdit.setText(reg_modal.registered_email)
            self.passWordEdit.setText(reg_modal.registered_password)

    def remember_me_widget(self):
        remember_me = CheckBox("Remember Me !")
        remember_me_data = Database().get_remember_me()
        if remember_me_data is not None:
            user_name_r = remember_me_data['user_name']
            pass_word_r = remember_me_data['pass_word']
            self.passWordEdit.setText(pass_word_r)
            self.userNameEdit.setText(user_name_r)
            remember_me.setChecked(True)
        return remember_me
