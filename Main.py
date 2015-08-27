__author__ = 'NamelessOne'
# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from unipath import Path
import shutil

# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QWidget, QMainWindow, QTextEdit, QPushButton, QLabel, QLineEdit, QAction, QApplication, \
    QFileDialog
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

ICON_FILE = 'open-file-icon.png'


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # This is my UI widget
        self.initUI()

    def initUI(self):
        label_ant = QLabel('Ant path', self)
        label_ant.move(20, 20)
        text_edit_ant = QLineEdit(self)
        text_edit_ant.move(20, 40)
        text_edit_ant.resize(420, 20)
        if os.environ.get('ANT_HOME'):
            text_edit_ant.setText(os.environ['ANT_HOME'])
        button_ant = QPushButton(self)
        button_ant.setIcon(QIcon(ICON_FILE))
        button_ant.move(450, 40)
        button_ant.resize(20, 20)
        button_ant.clicked.connect(lambda x: self.show_folder_choose_dialog(text_edit_ant.setText))

        label_sdk = QLabel('SDK path', self)
        label_sdk.move(20, 70)
        text_edit_sdk = QLineEdit(self)
        text_edit_sdk.move(20, 90)
        text_edit_sdk.resize(420, 20)
        if os.environ.get('ANDROID_HOME'):
            text_edit_sdk.setText(os.environ['ANDROID_HOME'])
        button_sdk = QPushButton(self)
        button_sdk.setIcon(QIcon(ICON_FILE))
        button_sdk.move(450, 90)
        button_sdk.resize(20, 20)
        button_sdk.clicked.connect(lambda x: self.show_folder_choose_dialog(text_edit_sdk.setText))

        label_keystore = QLabel('Keystore file path', self)
        label_keystore.move(20, 120)
        text_edit_keystore = QLineEdit(self)
        text_edit_keystore.move(20, 140)
        text_edit_keystore.resize(420, 20)
        button_keystore = QPushButton(self)
        button_keystore.setIcon(QIcon(ICON_FILE))
        button_keystore.move(450, 140)
        button_keystore.resize(20, 20)
        button_keystore.clicked.connect(lambda x: self.show_file_choose_dialog(text_edit_keystore.setText))

        label_template = QLabel('Template android project path', self)
        label_template.move(20, 170)
        text_edit_template = QLineEdit(self)
        text_edit_template.move(20, 190)
        text_edit_template.resize(420, 20)
        button_template = QPushButton(self)
        button_template.setIcon(QIcon(ICON_FILE))
        button_template.move(450, 190)
        button_template.resize(20, 20)
        button_template.clicked.connect(lambda x: self.show_folder_choose_dialog(text_edit_template.setText))

        ok_button = QPushButton('OK', self)
        ok_button.move(400, 450)
        ok_button.clicked.connect(
            lambda x: self.ok_click(text_edit_ant.text(), text_edit_sdk.text(), text_edit_keystore.text(),
                                    text_edit_template.text()))

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Ubiq android build setup')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

    def show_file_choose_dialog(self, set_text_function):
        file = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if len(file[0]) > 0:
            set_text_function(file[0])

    def show_folder_choose_dialog(self, set_text_function):
        folder = QFileDialog.getExistingDirectory(self, 'Open folder', '/home')
        if folder:
            set_text_function(folder)

    def ok_click(self, ant_path, sdk_path, keaystore_file, template_path):
        # TODO svn:ignore
        self.copy_files(Path(template_path).parent)
        self.write_changes(template_path)

    @staticmethod
    def copy_files(path):
        for file_name in os.listdir(os.getcwd() + '\scripts\\'):
            full_file_name = os.path.join(os.getcwd() + '\scripts\\', file_name)
            if os.path.isfile(os.path.join(os.getcwd() + '\scripts\\', file_name)):
                shutil.copy(full_file_name, path)

    def write_changes(self, template_path):
        # ant.propertines
        # local.properties
        # project.properties
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
