__author__ = 'NamelessOne'
from lxml import etree
from consts import *
from xml.dom.minidom import parse


class ManifestChanger:
    def __init__(self):
        self.MANIFEST_FILE = OUTPUT_DIR + "\\AndroidManifest.xml"

    def __remove_element(self, xpath):
        tree = etree.parse(self.MANIFEST_FILE)
        elem2 = tree.xpath(xpath, namespaces=NAMESPACE)
        elem2[0].getparent().remove(elem2[0])
        del elem2[:]
        tree.write(self.MANIFEST_FILE)

    def remove_activity(self, name):
        xpath = "/manifest/application/activity[@android:name='{}']".format(name)
        self.__remove_element(xpath)

    def set_version(self, new_version_code, new_version_name):
        dom1 = parse(self.MANIFEST_FILE)
        dom1.documentElement.setAttribute("android:versionCode", new_version_code)
        dom1.documentElement.setAttribute("android:versionName", new_version_name)
        with open(self.MANIFEST_FILE, 'wt') as f:
            f.write(dom1.toxml())
        f.close()

    def remove_receiver(self, name):
        xpath = "/manifest/application/receiver[@android:name='{}']".format(name)
        self.__remove_element(xpath)

    def remove_uses_permission(self, name):
        xpath = "/manifest/uses-permission[@android:name='{}']".format(name)
        self.__remove_element(xpath)

    def remove_permission(self, name):
        xpath = "/manifest/permission[@android:name='{}']".format(name)
        self.__remove_element(xpath)

    def remove_uses_feature(self, name):
        xpath = "/manifest/uses-feature[@android:name='{}']".format(name)
        self.__remove_element(xpath)

    def change_start_activity(self, name):
        tree = etree.parse(self.MANIFEST_FILE)
        xpath1 = "/manifest/application/activity[@android:name='.view.applicationactivity.ApplicationActivity']/intent-filter"
        xpath2 = "/manifest/application/activity[@android:name='{}']".format(name)
        elem1 = tree.xpath(xpath1, namespaces=NAMESPACE)
        elem2 = tree.xpath(xpath2, namespaces=NAMESPACE)
        elem2[0].append(elem1[0])
        tree.write(self.MANIFEST_FILE)