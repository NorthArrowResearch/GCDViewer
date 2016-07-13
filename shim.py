from gcdxml import GCDXML
from PyQt4.QtGui import QTreeView, QApplication, QWidget
import sys

app = QApplication(sys.argv)
w = QWidget() 

treeControl = QTreeView()
newGCD = GCDXML('/Users/matt/Desktop/gcd_project.gcd', treeControl)
print "DONE"
