import sys
from ui import Ui_Form

from db_handler import register, login, write_key_of_db, give_key_db, give_key_db_status

from cryptography.fernet import Fernet

from PyQt5 import QtCore, QtGui, QtWidgets

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import base64

#Initialization UI
app = QtWidgets.QApplication(sys.argv)

#Form creation
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

#Error Widget
def msg_box(text):
    Tk().withdraw()
    messagebox.showwarning("Alert", text)

#Get file
def give_file_home():
    Tk().withdraw()
    filename = askopenfilename()
    ui.lineEdit_3.setText(filename)

    get_status = give_key_db_status()

    if get_status:
        key = Fernet.generate_key() 
        give_status = write_key_of_db(key)

        if give_status:
            b = bytes(key, encoding='utf-8')
            key = base64.b64encode(b)

            ui.lineEdit_4.setText(str(key))
        else:
            ui.lineEdit_4.setText("Failed to get data!")

    else:
        key = give_key_db()
        ui.lineEdit_4.setText(str(key))


#Encryption function
def encoder():
    key = give_key_db()

    b = bytes(key, encoding='utf-8')

    cipher = Fernet(base64.b64encode(b))

    filename = ui.lineEdit_3.text()

    with open(filename, 'rw') as file:
        text = file.read()

        # Encrypt the file
        secured_text = cipher.encrypt(bytes(text))

        file.write(secured_text)
        msg_box("Success Encrypt!")

#Decrypt function
def decoder():
    try:
        key = give_key_db()

        b = bytes(key, encoding='utf-8')

        cipher = Fernet(base64.b64encode(b))

        filename = ui.lineEdit_3.text()

        with open(filename, 'rw') as file:
            text = file.read()

            # Decrypt the file
            secured_text = cipher.decrypt(bytes(text))

            file.write(secured_text)
            msg_box("Success Decrypt!")

    except Exception:
        print("Error")

#Disable registration menu after login
def toggle_menu_main(value):
    if value:
        ui.menu_register.setVisible(int(value))

#Send data to db_handler for registration
def reg():
    name = ui.lineEdit_5.text()
    password = ui.lineEdit_6.text()
    
    if name and password:
        toggle_menu_main(register(name, password))
    else:
        msg_box("Fill in the details!")

#Send data to db_handler for login
def auth():
    name = ui.lineEdit_5.text()
    password = ui.lineEdit_6.text()

    if name and password:
        toggle_menu_main(login(name, password))
    else:
        msg_box("Fill in the details!")

#Exit function
def exit():
    sys.exit(app.exec_())

#If the login button is clicked, call the auth() and reg() functions
ui.pushButton_7.clicked.connect( auth )
ui.pushButton_8.clicked.connect( reg )

#If the exit button is pressed, call the exit() function
ui.pushButton_3.clicked.connect( exit )

#If the file selection button is pressed, call the give_file_home() function
ui.pushButton_5.clicked.connect( give_file_home )

#If we click on the encryption button, we will call the encoder() function
ui.pushButton_4.clicked.connect( encoder )

#If we click on the decryption button, we will call the decoder() function
ui.pushButton_6.clicked.connect( decoder )

sys.exit(app.exec_())
