import os
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gcd_results_form.ui'))

class ResultsForm(QtGui.QDialog, FORM_CLASS):

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ResultsForm, self).__init__(parent)
        self.iface = iface
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setup_table()

    def setup_table(self):
        #set fonts
        #chaning the font creates some problems with header sizing that I haven't been able to resolve
        '''self.resultsTable.horizontalHeader().resizeSections(3)
        self.resultsTable.verticalHeader().resizeSections(3)
        font = QtGui.QFont()
        font.setFamily(u"Arial")
        font.setPointSize(4)
        self.resultsTable.horizontalHeader().setFont(font)
        self.resultsTable.verticalHeader().setFont(font)'''

        #set text form column and row labels
        self.resultsTable.setHorizontalHeaderLabels(["Raw","Thresholded","","Error Volume","%Error"])
        self.resultsTable.setVerticalHeaderLabels(["AREAL:","Total Area of Erosion (m^2)",
                                                   "Total Area of Deposition (m^2", "Total Area of Detectable Change (m^2)",
                                                   "Total Area of Interest (m^2)", "Percent of Area of Interest with Detectable Change",
                                                   "VOLUMETRIC:", "Total Volume of Erosion (m^3)",
                                                   "Total Volume of Deposition (m^3)", "Total Volume of Difference (m^3)",
                                                   "Total Net Volume Difference (m^3)",
                                                   "VERTICAL AVERAGES:", "Average Depth of Erosion (m)", "Average Depth of Deposition",
                                                   "Average Total Thickness of Difference (m) for Area of Interest",
                                                   "Average Net Thickness of Difference (m) for Area of Interest",
                                                   "Average Total Thickness of Difference (m) for Area with Detectable Change",
                                                   "Average Net Thickness of Difference (m) for Area with Detectable Change",
                                                   "PERCENTAGES (BY VOLUME):","Percent Erosion","Percent Deposition",
                                                   "Percent Imbalance (departure from equilibrium)", "Net to Total Volume Ratio"])