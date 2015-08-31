__author__ = 'NamelessOne'
# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from unipath import Path
import shutil
import fileinput

# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QWidget, QMainWindow, QTextEdit, QPushButton, QLabel, QLineEdit, QAction, QApplication, \
    QFileDialog
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from subprocess import check_call
from cd import cd

ICON_FILE = 'open-file-icon.png'


def write_properties(sdk_path, template_path, keystore_file, keystore_alias, keystore_password,
                     alias_password):
    ant_prop = open(template_path + '/ant.properties', 'w+')
    ant_prop.write('key.store=' + keystore_file)
    ant_prop.write('key.alias=' + keystore_alias)
    ant_prop.write('key.store.password=' + keystore_password)
    ant_prop.write('key.alias.password=' + alias_password)
    local_prop = open(template_path + '/ant.properties', 'w+')
    local_prop.write('sdk.dir=' + sdk_path)
    project_prop = open(template_path + '/ant.properties', 'w+')
    project_prop.write(
        'android.library.reference.1=' + sdk_path +
        '/extras/google/google_play_services/libproject/google-play-services_lib')
    project_prop.write('target=android-21')


def set_svn_ignore_files(template_path):
    # TODO ????????? ??????
    with cd(template_path):
        check_call("svn update --set-depth exclude local.properties")
        check_call("svn update --set-depth exclude ant.properties")
        check_call("svn update --set-depth exclude project.properties")


def copy_script_files(path):
    for file_name in os.listdir(os.getcwd() + '\scripts\\'):
        full_file_name = os.path.join(os.getcwd() + '\scripts\\', file_name)
        if os.path.isfile(os.path.join(os.getcwd() + '\scripts\\', file_name)):
            shutil.copy(full_file_name, path)


def first_build():
    check_call("build")


def copy_dexed_libs():
    # TODO
    pass


def change_consts_py(path, input_file):
    with cd(path):
        for line in fileinput.input("consts.py", inplace=True):
            if line.startswith('INPUT_DIR'):
                print('INPUT_DIR = ' + Path(input_file).parent)
            elif line.startswith('CONFIG_FILE'):
                print('CONFIG_FILE = ' + input_file)
            else:
                print(line)
        pass
    pass


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # This is my UI widget
        self.initUI()

    def initUI(self):
        label_config = QLabel('Build config file', self)
        label_config.move(20, 20)
        text_edit_config = QLineEdit(self)
        text_edit_config.move(20, 40)
        text_edit_config.resize(420, 20)
        button_config = QPushButton(self)
        button_config.setIcon(QIcon(ICON_FILE))
        button_config.move(450, 40)
        button_config.resize(20, 20)
        button_config.clicked.connect(lambda x: self.show_file_choose_dialog(text_edit_config.setText))

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

        label_keystore = QLabel('Keystore file', self)
        label_keystore.move(20, 120)
        text_edit_keystore = QLineEdit(self)
        text_edit_keystore.move(20, 140)
        text_edit_keystore.resize(420, 20)
        button_keystore = QPushButton(self)
        button_keystore.setIcon(QIcon(ICON_FILE))
        button_keystore.move(450, 140)
        button_keystore.resize(20, 20)
        button_keystore.clicked.connect(lambda x: self.show_file_choose_dialog(text_edit_keystore.setText))

        label_alias = QLabel('Keystore alias', self)
        label_alias.move(20, 170)
        text_edit_alias = QLineEdit(self)
        text_edit_alias.move(20, 190)
        text_edit_alias.resize(420, 20)

        label_password = QLabel('Keystore password', self)
        label_password.move(20, 220)
        text_edit_password = QLineEdit(self)
        text_edit_password.move(20, 240)
        text_edit_password.resize(420, 20)

        label_alias_password = QLabel('Keystore alias password', self)
        label_alias_password.move(20, 270)
        text_edit_alias_password = QLineEdit(self)
        text_edit_alias_password.move(20, 290)
        text_edit_alias_password.resize(420, 20)

        label_template = QLabel('Template android project path', self)
        label_template.move(20, 320)
        text_edit_template = QLineEdit(self)
        text_edit_template.move(20, 340)
        text_edit_template.resize(420, 20)
        button_template = QPushButton(self)
        button_template.setIcon(QIcon(ICON_FILE))
        button_template.move(450, 340)
        button_template.resize(20, 20)
        button_template.clicked.connect(lambda x: self.show_folder_choose_dialog(text_edit_template.setText))

        ok_button = QPushButton('OK', self)
        ok_button.move(400, 450)
        ok_button.clicked.connect(
            lambda x: self.ok_click(text_edit_config.text(), text_edit_sdk.text(), text_edit_keystore.text(),
                                    text_edit_alias.text(), text_edit_password.text(), text_edit_alias_password.text(),
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

    def ok_click(self, config_file, sdk_path, keystore_file, alias, password, alias_password, template_path):
        copy_script_files(Path(template_path).parent)
        set_svn_ignore_files(template_path)
        write_properties(sdk_path, template_path, keystore_file, alias, password, alias_password)
        change_consts_py(Path(template_path).parent)
        first_build()
        copy_dexed_libs()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
