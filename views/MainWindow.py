import asyncio

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QFrame, QLineEdit, QPushButton, QTextBrowser, QComboBox, QMessageBox, \
    QApplication, QCheckBox
from requests.exceptions import HTTPError

from core.aduana import request_aduana
from pathlib import Path


class MainWindow(QFrame):
    Frame: QFrame
    awb_lineEdit: QLineEdit
    house_lineEdit: QLineEdit
    mnft_number_lineEdit: QLineEdit
    mnft_year_lineEdit: QLineEdit
    submit_btn: QPushButton
    boletin_info: QTextBrowser
    database_select: QComboBox
    house_checkbox: QCheckBox

    def __init__(self) -> None:
        super(QFrame, self).__init__()
        template = Path('templates/Main.ui').__str__()
        uic.loadUi(template, self)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        only_integers = QIntValidator()
        self.awb_lineEdit.setValidator(only_integers)
        self.house_lineEdit.setValidator(only_integers)
        self.mnft_number_lineEdit.setValidator(only_integers)
        self.mnft_year_lineEdit.setValidator(only_integers)
        self.awb_lineEdit.textChanged.connect(self.add_dash_event)
        self.awb_lineEdit.textEdited.connect(self.enable_submit_button_event)
        self.house_lineEdit.textEdited.connect(self.enable_submit_button_event)
        self.mnft_year_lineEdit.textEdited.connect(self.enable_submit_button_event)
        self.mnft_number_lineEdit.textEdited.connect(self.enable_submit_button_event)
        self.submit_btn.clicked.connect(self.submit_form_event)
        self.house_checkbox.stateChanged.connect(self.enable_house_field)

        self.mnft_number_lineEdit.setText("6265")
        self.mnft_year_lineEdit.setText("2023")
        self.awb_lineEdit.setText("136-62632496")
        self.house_lineEdit.setText("99179964")

    def add_dash_event(self, text):
        if len(text) == 3:
            self.awb_lineEdit.setText(text + "-")
        elif len(text) > 4:
            self.awb_lineEdit.setText(text)

    def enable_submit_button_event(self):
        enabled = len(self.awb_lineEdit.text()) == 12 and len(self.mnft_number_lineEdit.text()) and len(self.mnft_year_lineEdit.text())
        if self.house_checkbox.isChecked():
            enabled = enabled and 3 <= len(self.house_lineEdit.text()) <= 12
        self.submit_btn.setEnabled(enabled)

    def enable_fields(self, enable: bool):
        self.submit_btn.setEnabled(enable)
        self.awb_lineEdit.setEnabled(enable)
        self.database_select.setEnabled(enable)
        self.mnft_number_lineEdit.setEnabled(enable)
        self.mnft_year_lineEdit.setEnabled(enable)
        self.house_checkbox.setEnabled(enable)
        if self.house_checkbox.isChecked():
            self.house_lineEdit.setEnabled(enable)
        QApplication.processEvents()

    def enable_house_field(self,enable):
        self.house_lineEdit.setEnabled(enable)
        self.enable_submit_button_event()



    def submit_form_event(self):
        self.enable_fields(False)
        asyncio.run(self.request_buletin())
        self.enable_fields(True)

    async def request_buletin(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()

        mnft_year = self.mnft_year_lineEdit.text()
        mnft_number = self.mnft_number_lineEdit.text()
        awb = self.awb_lineEdit.text()
        house = self.house_lineEdit.text()
        self.boletin_info.clear()
        try:
            codigo_carga = f'{awb} {house}' if self.house_checkbox.isChecked() else awb
            response = request_aduana(self.database_select.currentText(), f'{mnft_number}/{mnft_year}',codigo_carga)
            QApplication.restoreOverrideCursor()
            self.show_aduana_response(response)
        except HTTPError as e:
            QApplication.restoreOverrideCursor()
            response = e.response
            if response.status_code == 400:
                self.show_exception_message_box(response.text)
            else:
                self.show_exception_message_box(e.__str__())

    def show_aduana_response(self, response):
        self.show_buletin_info(response)
        messagebox = QMessageBox()
        messagebox.setWindowModality(Qt.WindowModality.ApplicationModal)
        messagebox.setWindowTitle('Respuesta de aduana')

        if not response['success']:
            messagebox.setText(response['msg'])
            messagebox.setIcon(QMessageBox.Icon.Critical)
        else:
            messagebox.setText('Boletin cargado correctamente')
            messagebox.setIcon(QMessageBox.Icon.Information)
        messagebox.exec()

    def show_exception_message_box(self, message: str):
        messagebox = QMessageBox()
        messagebox.setWindowModality(Qt.WindowModality.ApplicationModal)
        messagebox.setIcon(QMessageBox.Icon.Critical)
        messagebox.setWindowTitle('Ha ocurrido un error')
        messagebox.setText(message)
        messagebox.exec()

    def show_buletin_info(self, response):
        if not response['success']:
            self.boletin_info.setMarkdown(response['msg'])
        else:
            despacho = response['despachos'][0]
            self.boletin_info.setMarkdown(f"### Numero de ticket: {despacho['BOLETIN_DERECHO']}\n"
                                          f"### Valor de Servicio: {despacho['VALOR_SERVICIO']}\n"
                                          f"### Valor de Arancel: {despacho['VALOR_DERECHOS']}\n")
