from distutils.core import setup
import sys
import os
import py2exe
from unipath import Path

script_files = []
for file in os.listdir(os.getcwd()+'\scripts'):
    f1 = os.getcwd()+'\scripts\\' + file
    if os.path.isfile(f1): # skip directories
        script_files.append(f1)

setup(
    windows=[{"script": "Main.py"}],
    data_files=[('platforms',
                [Path(sys.executable).parent + '\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll',]),
                ('', ['open-file-icon.png',]), ('scripts', script_files)],
    name='AndroidBuildInstaller',
    packages=[''],
    author='NamelessOne'
)
# TODO /platforms/qwindows.dll ?? Python34\Lib\site-packages\PyQt5\plugins
'''
C:/Users/NamelessOne/PycharmProjects/AndroidBuildInstaller/python setup.py py2ex
e --includes sip
'''