# -*- coding: utf-8 -*-
"""
/***************************************************************************
This class is responsible for loading and maintining the GCD project file

"""

import os
from PyQt4 import QtGui
from PyQt4.QtGui import QStandardItem, QStandardItemModel, QTreeView, QMessageBox, QIcon, QPixmap
from PyQt4.QtCore import *
import xml.etree.ElementTree as ET

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
            # Set up an invisible root item for the tree.
            #self.treeRoot = self.model.invisibleRootItem()
            self.treeRoot = QStandardItem("Root Item")
            self.model.appendRow(self.treeRoot)
            self.tree.setModel(self.model)
            self.tree.setDragEnabled(True)

            # This is the GCD projet viewer so no harm in hardcoding this for now.
            self.xmlTreePath = os.path.join(os.path.dirname(__file__), "Resources/XML/gcd_tree.xml")
            self.xmlProjPath = xmlPath
            self.namespaces = {'http://tempuri.org/ProjectDS.xsd'}

            # Load the tree file (the rules we use to build the tree)
            self.xmlTemplateDoc = ET.parse(self.xmlTreePath)
            # Load the GCD Project (the raw data that will be used to populate the tree)
            self.xmlProjectDoc = ET.parse(self.xmlProjPath)
            
            # Set up the first domino for the recursion            
            self.LoadNode(None, self.xmlTemplateDoc.find("node"), self.xmlProjectDoc.getroot())

#     def Load(self):
#         for demSurvey in xmldoc.getElementsByTagName('DEMSurvey'):
#             nameNode = demSurvey.getElementsByTagName('Name')[0]
#             demSurveyitem = self.add_item(self.rootItem, self.getNodeText(nameNode))
#             
#             for assocSurface in demSurvey.getElementsByTagName('AssociatedSurface'):
#                 if len(assocSurface.getElementsByTagName('Name')) > 0:
#                     name = self.getNodeText(assocSurface.getElementsByTagName('Name')[0])
#                     assocSurfaceItem = self.add_item(demSurveyitem, name)
#             
#         print "booya"
        
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
    
    
    def LoadRepeater(self, tnParent, templateNode, projNode):
        """ Repeater is for using an XPAth in the project file for repeating elements"""
        
        print("------- LOAD Repeater---------")
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
            print "XPATH:: ", xpath.text, "  Absolute? ", absoluteXPath 
            if absoluteXPath:
                xNewProjList = self.xmlProjectDoc.findall(xpath.text)
            else:
                xNewProjList = projNode.findall(xpath.text)

        print "NEWPROJLIST:::" , xNewProjList
        for xProjChild in xNewProjList:
            self.LoadNod(newTreeItem, xPatternNode, xProjChild)
                        
    def LoadNode(self, tnParent, templateNode, projNode):
        """ Load a single node """
        print("------- LOAD NODE---------")
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
        
        print "SEARCH DEBUG:: ", templateNode.findall("children/repeater", self.namespaces)
        
        # Just a regular node with children
        for xChild in templateNode.findall("children/node"):
            print "REGULAR CHILD FOUND", xChild
            self.LoadNode(newTreeItem, xChild, newProjNode)
        for xRepeater in templateNode.findall("children/repeater"):
            print "REPEATER FOUND", xRepeater
            self.LoadRepeater(newTreeItem, xRepeater, newProjNode)

    
    
    def getLabel(self, templateNode, projNode):
        """ Either use the liral text inside <label> or look it
            up in the project node if there's a <label xpath="/x/path">
        """
        labelNode = templateNode.find("label")
        label = "TITLE_NOT_FOUND"
        if labelNode is not None:
            if "xpath" in labelNode.attrib:
                xpath = labelNode.attrib['xpath']
                label = projNode.find(xpath, self.namespaces).text
            else:
                label = labelNode.text      
                
        return label