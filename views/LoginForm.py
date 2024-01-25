import typing

import asyncio
from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QWidget, QComboBox, QLineEdit, QPushButton
from PyQt6 import uic


class LoginForm(QFrame):
    select_database:QComboBox
    select_users:QComboBox
    password_field:QLineEdit
    login_btn:QPushButton
    exit_btn:QPushButton

    def __init__(self) -> None:
        super(LoginForm, self).__init__()
        uic.loadUi('templates/LoginForm.ui',self)
        self.show()

    async def _loadDatabases(self):
        await asyncio.sleep(3)
        databases = [
            {'text':'La Habana','data':'HAV'},
            {'text':'Santiago de Cuba','data':'S'},
            {'text':'Varadero','data':'VRA'},
        ]
        self.select_database.clear()
        for database in databases:
            self.select_database.addItem(database['text'],database['data'])