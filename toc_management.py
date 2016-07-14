import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *

from qgis.core import QgsMapLayer, QgsRasterLayer, QgsMapLayerRegistry,QgsProject

# http://www.lutraconsulting.co.uk/blog/2014/07/25/qgis-layer-tree-api-part-2/

def AddGroup(sGroupName, parentGroup):
    
    # If no parent group specified then the parent is the ToC tree root
    if not parentGroup:
        parentGroup =  QgsProject.instance().layerTreeRoot()

    # Attempt to find the specified group in the parent
    thisGroup = parentGroup.findGroup(sGroupName)
    if not thisGroup:
        thisGroup = parentGroup.insertGroup(0, sGroupName)

    return thisGroup

def AddRasterLayer(theRaster):

    # Loop over all the parent group layers for this raster
    # ensuring they are in the tree in correct, nested order
    parentGroup = None
    for aGroup in theRaster.data()["group_layers"]:
        parentGroup = AddGroup(aGroup, parentGroup)

    assert parentGroup, "All rasters should be nested and so parentGroup should be instantiated by now"

    # Only add the layer if it's not already in the registry
    if not QgsMapLayerRegistry.instance().mapLayersByName(theRaster.text()):
        rOutput = QgsRasterLayer(theRaster.data()["filepath"], theRaster.text())
        QgsMapLayerRegistry.instance().addMapLayer(rOutput, False)
        parentGroup.addLayer(rOutput)

        # call Konrad's symbology method here using data()["symbology"]

    # if the layer already exists trigger a refresh
    else:
        thisLayer.triggerRepaint()
