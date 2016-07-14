# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GCDViewerDockWidget
                                 A QGIS plugin
 View GCD Files
                             -------------------
        begin                : 2016-07-12
        git sha              : $Format:%H$
        copyright            : (C) 2016 by NorthArrowResearch
        email                : info@northarrowresearch.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from gcdxml import GCDXML
from gcd_results_form import ResultsForm

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gcd_viewer_dockwidget_base.ui'))


class GCDViewerDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(GCDViewerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.resultsDialog = ResultsForm(iface)
        self.btnLoad.clicked.connect(self.raster_file_browser)
        self.btn_results.clicked.connect(self.resultsEvent)
        #         self.xmlLocation
        #         self.treeView =

    def raster_file_browser(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open GCD file", "", "GCD File (*.gcd);;All files (*)")
        filename = os.path.splitext(str(filename))[0]+".gcd"
        self.xmlLocation.setText(filename)
        self.gcdxml = GCDXML(filename, self.treeView)
        self.recalc_state()    

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def resultsEvent(self, event):
        self.resultsDialog.exec_()

    def recalc_state(self):
        print "recalc state"
