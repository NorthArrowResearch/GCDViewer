# -*- coding: utf-8 -*-
"""
/***************************************************************************
This class is responsible for loading and maintining the GCD project file

"""

import os
from PyQt4 import QtGui
from PyQt4.QtGui import QStandardItem, QStandardItemModel, QTreeView, QMessageBox, QIcon, QPixmap
from PyQt4.QtCore import *
from xml.dom import minidom

class GCDXML():
    
    def __init__(self, xmlPath, parent = None):
        """Constructor"""
        if xmlPath is None or not os.path.isfile(xmlPath):
            msg = "..."
            q = QMessageBox(QMessageBox.Warning, "Could not find that file",  msg)
            q.setStandardButtons(QMessageBox.Ok);
            i = QIcon()
            i.addPixmap(QPixmap("..."), QIcon.Normal)
            q.setWindowIcon(i)
            q.exec_()
        else:
            self.domtree = QTreeView(self)
            self.view.setDragEnabled(True)
            self.Load(xmlPath)

    def Load(self, path):
        xmldoc = minidom.parse(path)

        for node in xmldoc.getElementsByTagName('DEMSurvey'):
            itemName = node.getElementsByTagName('Name')
            print(self.getNodeText(itemName[0]))
        
        print "booya"
        
    def getNodeText(self, node):
        nodelist = node.childNodes
        result = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                result.append(node.data)
        return ''.join(result)