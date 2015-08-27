__author__ = 'NamelessOne'

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = ROOT_DIR + '\input'
OUTPUT_DIR = ROOT_DIR + '\output'
TEMPLATE_DIR = ROOT_DIR + '\\Android Client'
CONFIG_FILE = 'schema.cfg'
OLD_PACKAGE_NAME = 'com.ubiqmobile.client'
OLD_PACKAGE_DIR = '\\com\\ubiqmobile\\client'
DIRECTIVE_START = '//STARTCUSTOMBUILD_'
DIRECTIVE_END = '//ENDCUSTOMBUILD_'
ZBAR_LIB_DIRECTIVE = 'ZBAR'
LOCATION_DIRECTIVE = 'LOCATION'
GCM_DIRECTIVE = 'GCM'
JAVA_SOURCES_ENCODING = 'utf_8'
NAMESPACE = {'android': 'http://schemas.android.com/apk/res/android'}
SRC_DIRECTORY = OUTPUT_DIR + '\\src'
RES_DIR = OUTPUT_DIR + '\\res'
VALUES_DIR_MASK = 'values-'
STRING_FILENAME = 'strings_ubiq.xml'
