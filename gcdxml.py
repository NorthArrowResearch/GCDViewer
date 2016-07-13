# -*- coding: utf-8 -*-
"""
/***************************************************************************
This class is responsible for loading and maintining the GCD project file

"""

import os
from PyQt4 import QtGui
from PyQt4.QtGui import QStandardItem, QMenu, QStandardItemModel, QTreeView, QMessageBox, QIcon, QPixmap
from PyQt4.QtCore import *
from StringIO import StringIO
import xml.etree.ElementTree as ET

class GCDXML():
    
    def __init__(self, xmlPath, treeControl, parent = None):
        """ Constructor """
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
            # Set up an invisible root item for the tree.
            #self.treeRoot = self.model.invisibleRootItem()
            self.treeRoot = QStandardItem("Root Item")
            self.model.appendRow(self.treeRoot)
            self.tree.setModel(self.model)
            self.tree.doubleClicked.connect(self.item_doubleClicked)
            self.tree.customContextMenuRequested.connect(self.openMenu)
            self.tree.setDragEnabled(True)

            # This is the GCD projet viewer so no harm in hardcoding this for now.
            self.xmlTreePath = os.path.join(os.path.dirname(__file__), "Resources/XML/gcd_tree.xml")
            self.xmlProjPath = xmlPath

            self.namespace = "{http://tempuri.org/ProjectDS.xsd}"

            # Load the tree file (the rules we use to build the tree)
            self.xmlTemplateDoc = ET.parse(self.xmlTreePath)
            # Load the GCD Project (the raw data that will be used to populate the tree)
            # instead of ET.fromstring(xml)
            with open(self.xmlProjPath, 'r') as myfile:
                data=myfile.read().replace('\n', '')
                it = ET.iterparse(StringIO(data))
                for _, el in it:
                    if '}' in el.tag:
                        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
                self.xmlProjectDoc = it.root
            
            # Set up the first domino for the recursion            
            self.LoadNode(None, self.xmlTemplateDoc.find("node"), self.xmlProjectDoc)
            self.tree.expandToDepth(5)
            
    def add_item(self, parent, text, meta):
        """ Add an item to the tree """ 
        if len(text) > 0: 
            item = QStandardItem(text)
            if meta is not None:
                print meta
            parent.appendRow(item)
            parent.setExpanded(True)
            return item
                    
                        
    def LoadNode(self, tnParent, templateNode, projNode):
        """ Load a single node """
        
        label = self.getLabel(templateNode, projNode)

        newTreeItem = QStandardItem(label)
        if tnParent is None:
            self.treeRoot.appendRow(newTreeItem)
        else:
            tnParent = tnParent.appendRow(newTreeItem)

        # Detect if this is an XML node element and reset the root Project node to this.
        entityType = templateNode.find('entity/type')
        entityXPath = templateNode.find('entity/xpath')
        newProjNode = projNode
        if (entityXPath):
            newProjNode = projNode.find(entityXPath)        
                
        # Just a regular node with children
        for xChild in templateNode.findall("children/node"):
            self.LoadNode(newTreeItem, xChild, newProjNode)
        for xRepeater in templateNode.findall("children/repeater"):
            self.LoadRepeater(newTreeItem, xRepeater, newProjNode)


    def LoadRepeater(self, tnParent, templateNode, projNode):
        """ Repeater is for using an XPAth in the project file for repeating elements """
        
        label = self.getLabel(templateNode, projNode)
        
        newTreeItem = QStandardItem(label)
        if tnParent is None:
            self.treeRoot.appendRow(newTreeItem)
        else:
            tnParent = tnParent.appendRow(newTreeItem)                
            
        # REmember, repeaters can only contain one "pattern" node
        xPatternNode = templateNode.find("node")

        # If there is an Xpath then reset the base project node to that.   
        xpath = templateNode.find("xpath")
        xNewProjList = []
        if xPatternNode is not None and xpath is not None:
            absoluteXPath = xpath.text[:1] == "/"
            # Should we search from the root or not.
            if absoluteXPath:
                xNewProjList = self.xmlProjectDoc.findall("." + xpath.text)
            else:
                xNewProjList = projNode.findall(xpath.text)

        for xProjChild in xNewProjList:
            self.LoadNode(newTreeItem, xPatternNode, xProjChild)    
    
    def item_doubleClicked(self, index):
        item = self.tree.selectedIndexes()[0]
        print "DOUBLE CLICKED" , item.model().itemFromIndex(index).text()
        self.addToMap( item.model().itemFromIndex(index))
    
    def openMenu(self, position):
        indexes = self.tree.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QMenu()
        if level == 0:
            menu.addAction("Edit person")
        elif level == 1:
            menu.addAction("Edit object/container")
        elif level == 2:
            menu.addAction("Edit object")
         
        menu.exec_(self.tree.viewport().mapToGlobal(position))
    
    def getLabel(self, templateNode, projNode):
        """ Either use the liral text inside <label> or look it
            up in the project node if there's a <label xpath="/x/path">
        """
        labelNode = templateNode.find("label")
        label = "TITLE_NOT_FOUND"
        if labelNode is not None:
            if "xpath" in labelNode.attrib:
                xpath = labelNode.attrib['xpath']
                label = projNode.find(xpath).text
            else:
                label = labelNode.text      
                
        return label
    
    def addToMap(self, item):
        print "ADDING TO MAP::", item.text()