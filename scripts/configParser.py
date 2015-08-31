# -*- coding: utf-8 -*-

__author__ = 'NamelessOne'
import shutil
import codecs
import distutils.core
import json
from AndroidManifestChanger import ManifestChanger
from consts import *
from lxml import etree
from tempfile import mkstemp
from shutil import move
from os import close, remove, rmdir

manifestChanger = ManifestChanger()


def process_dir(directory):
    for folder, subFolders, files in os.walk(directory):
        for file in files:
            process_file(folder + "/" + file)
        for subFolder in subFolders:
            process_dir(subFolder)


def process_file(file):
    if str(file).endswith(CONFIG_FILE):
        process_config_file(file)
    else:
        process_non_xml_file(file)


def process_config_file(file):
    f = codecs.open(file, 'r', JAVA_SOURCES_ENCODING)
    json_data = f.read()
    data = json.loads(json_data)
    distutils.dir_util.copy_tree(TEMPLATE_DIR,
                                 OUTPUT_DIR)
    manifestChanger.set_version(data['VersionCode'], data['VersionName'])
    process_locales(data['locales'])
    process_need_barcode(data['barcodeNeeded'])
    process_need_location(data['locationNeeded'])
    process_need_gcm(data['gcmNeeded'])
    # !!!
    process_package_name(data['package'])
    if data['splashScreen'] == 'true':
        # Splash Screen. Change start activity (from MainActivity to SplashScreenActivity)
        manifestChanger.change_start_activity('.view.applicationactivity.SplashScreenActivity')
    xml_changes = data['xmlChanges']
    for xmlChange in xml_changes:
        changes = xmlChange['changes']
        for change in changes:
            process_change(xmlChange['file'], change['value'], change['xpath'])


def process_non_xml_file(file):
    output_file = str(file.replace(INPUT_DIR, OUTPUT_DIR))
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    shutil.copyfile(file, output_file)
    # print(file)


def process_need_barcode(barcode_needed):
    if barcode_needed.lower() in "true":
        pass
    else:
        # Удаляем zBar и его ошмётки
        remove(OUTPUT_DIR + '\\libs\\armeabi\\libzbarjni.so')
        remove(OUTPUT_DIR + '\\libs\\armeabi\\libiconv.so')
        remove(OUTPUT_DIR + '\\libs\\armeabi-v7a\\libzbarjni.so')
        remove(OUTPUT_DIR + '\\libs\\armeabi-v7a\\libiconv.so')
        remove(OUTPUT_DIR + '\\libs\\x86\\libzbarjni.so')
        remove(OUTPUT_DIR + '\\libs\\x86\\libiconv.so')
        remove(OUTPUT_DIR + '\\libs\\zbar.jar')
        remove(OUTPUT_DIR + '\\libs\\zbarscanner.jar')
        remove(
            SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\BarcodeCommandManager.java')
        # Тут в ApplicationActivityViewModal удаляем ошмётки zBar
        remove_some_code(ZBAR_LIB_DIRECTIVE)
        # Еще нужно из манифеста его снести
        manifestChanger.remove_activity('com.dm.zbar.android.scanner.ZBarScannerActivity')
        '''
        #Камеру удалять только если не нужно чтение баркодов И передача видео с телефона
        manifestChanger.remove_uses_feature('android.hardware.camera')
        manifestChanger.remove_uses_feature('android.hardware.camera.front')
        manifestChanger.remove_uses_feature('android.hardware.camera.autofocus')
        manifestChanger.remove_uses_feature('android.hardware.camera.flash')
        manifestChanger.remove_uses_permission('android.permission.CAMERA')
        manifestChanger.remove_uses_permission('android.permission.FLASHLIGHT')
        '''


def process_need_location(location_needed):
    if location_needed.lower() in "true":
        pass
    else:
        remove(
            SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\location\\LocationCommandManager.java')
        remove(
            SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\location\\AbstractUserLocationManager.java')
        remove(SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\location\\ILocationAware.java')
        remove(SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\location\\LocationListener.java')
        remove(SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\managers\\location\\UserLocationManager.java')
        remove_some_code(LOCATION_DIRECTIVE)
        manifestChanger.remove_uses_permission('android.permission.ACCESS_FINE_LOCATION')
        manifestChanger.remove_uses_permission('android.permission.ACCESS_COARSE_LOCATION')
        manifestChanger.remove_uses_feature('android.hardware.location.gps')
        manifestChanger.remove_uses_feature('android.hardware.location.network')
        manifestChanger.remove_uses_feature('android.hardware.location')


def process_need_gcm(gcm_needed):
    if gcm_needed.lower() in "true":
        pass
    else:
        remove(SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\UbiqGcmBroadcastReceiver.java')
        remove(SRC_DIRECTORY + OLD_PACKAGE_DIR + '\\internal\\controller\\UbiqGcmIntentService.java')
        remove_some_code(GCM_DIRECTIVE)
        replace_line_in_file(OUTPUT_DIR + '\\ant_build.xml',
                             '<path path="${sdk.dir}/extras/google/google_play_services/libproject/google-play-services_lib/libs/google-play-services.jar" />',
                             '')
        manifestChanger.remove_receiver('.internal.controller.UbiqGcmBroadcastReceiver')
        manifestChanger.remove_uses_permission('com.google.android.c2dm.permission.RECEIVE')
        manifestChanger.remove_uses_permission('android.permission.GET_ACCOUNTS')
        manifestChanger.remove_uses_permission('com.ubiqmobile.client.permission.C2D_MESSAGE')
        manifestChanger.remove_permission('com.ubiqmobile.client.permission.C2D_MESSAGE')
        manifestChanger.remove_uses_permission('android.permission.READ_CONTACTS')
        manifestChanger.remove_uses_permission('android.permission.VIBRATE')
        # TODO не запускать googleplay-version-grabber
        # TODO удалить из манифеста meta-data


def process_locales(locales):
    folder_locales = []
    for folder, subFolders, files in os.walk(RES_DIR):
        for subFolder in subFolders:
            if VALUES_DIR_MASK in subFolder:
                folder_locales.append(subFolder.split('-')[1])
    for locale in locales:
        if locale not in folder_locales:
            # создаём папку
            os.mkdir(RES_DIR + '\\' + VALUES_DIR_MASK + locale)
            # и копируем туда содержимое default локали
            shutil.copyfile(RES_DIR + '\\' + VALUES_DIR_MASK.split('-')[0] + '\\' + STRING_FILENAME,
                            RES_DIR + '\\' + VALUES_DIR_MASK + locale + '\\' + STRING_FILENAME)
            pass
    for locale in folder_locales:
        if locale not in locales:
            # удаляем папку с ненужной локалью
            remove(RES_DIR + '\\' + VALUES_DIR_MASK + locale + '\\' + STRING_FILENAME)
            rmdir(RES_DIR + '\\' + VALUES_DIR_MASK + locale)
            pass


def process_package_name(name):
    print('packageName = ' + name)
    dir_name = '\\' + str(name).replace('.', '\\')
    old_dir_name = SRC_DIRECTORY + OLD_PACKAGE_DIR
    shutil.move(old_dir_name, old_dir_name.replace(OLD_PACKAGE_DIR, dir_name))
    manifest = OUTPUT_DIR + "\\AndroidManifest.xml"
    replace(manifest, OLD_PACKAGE_NAME, name)
    for folder, subFolders, files in os.walk(SRC_DIRECTORY):
        for file in files:
            replace(folder + "\\" + file, OLD_PACKAGE_NAME, name)
    replace(OUTPUT_DIR + '\\res\\layout\\application_activity.xml', OLD_PACKAGE_NAME, name)
    replace(OUTPUT_DIR + '\\res\\xml\\main_preferences.xml', OLD_PACKAGE_NAME, name)


def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    new_file = codecs.open(abs_path, 'w', JAVA_SOURCES_ENCODING)
    old_file = codecs.open(file_path, 'r', JAVA_SOURCES_ENCODING)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    # close temp file
    new_file.close()
    close(fh)
    old_file.close()
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def process_change(file, value, xpath):
    tree = etree.parse(OUTPUT_DIR + '\\' + file.replace('/', '\\'))
    # ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
    # root = tree.getroot()
    elem = tree.xpath(xpath, namespaces=NAMESPACE)
    elem[0].getparent().text = value
    tree.write(OUTPUT_DIR + '\\' + file.replace('/', '\\'))


def remove_some_code(directive):
    process_dir_for_replacing_code(SRC_DIRECTORY, directive)


def process_dir_for_replacing_code(directory, directive):
    for folder, subFolders, files in os.walk(directory):
        for file in files:
            replace_line_in_file(folder + "\\" + file, DIRECTIVE_START + directive, '/*')
            replace_line_in_file(folder + "\\" + file, DIRECTIVE_END + directive, '*/')
        for subFolder in subFolders:
            process_dir_for_replacing_code(subFolder, directive)


def replace_line_in_file(file_name, source_text, replace_text):
    file = open(file_name, 'r', encoding=JAVA_SOURCES_ENCODING)  # Opens the file in read-mode
    text = file.read()  # Reads the file and assigns the value to a variable
    file.close()  # Closes the file (read session)
    file = open(file_name, 'w', encoding=JAVA_SOURCES_ENCODING)  # Opens the file again, this time in write-mode
    file.write(text.replace(source_text, replace_text))  # replaces all instances of our keyword
    # and writes the whole output when done, wiping over the old contents of the file
    file.close()  # Closes the file (write session)
    # print('All went well, the modifications are done in file ' + fileName)


# ---------------------MAIN--------------------------
process_dir(INPUT_DIR)
print('processing config file complete')
