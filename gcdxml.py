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
    
    def __init__(self, xmlPath, treeControl, parent = None):
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
            self.tree = treeControl
            self.model = QStandardItemModel()
            self.rootItem = self.model.invisibleRootItem()
            self.tree.setModel(self.model)
            self.tree.setDragEnabled(True)
            self.Load(xmlPath)

    def Load(self, path):
        xmldoc = minidom.parse(path)
        
        for demSurvey in xmldoc.getElementsByTagName('DEMSurvey'):
            nameNode = demSurvey.getElementsByTagName('Name')[0]
            demSurveyitem = self.add_item(self.rootItem, self.getNodeText(nameNode))
            
            for assocSurface in demSurvey.getElementsByTagName('AssociatedSurface'):
                if len(assocSurface.getElementsByTagName('Name')) > 0:
                    name = self.getNodeText(assocSurface.getElementsByTagName('Name')[0])
                    assocSurfaceItem = self.add_item(demSurveyitem, name)
            
        print "booya"
        
    def add_item(self, parent, text):
        if len(text) > 0: 
            item = QStandardItem(text)
            parent.appendRow(item)
            return item
        
    def getNodeText(self, node):
        nodelist = node.childNodes
        result = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                result.append(node.data)
        return ''.join(result)