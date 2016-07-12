# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GCDViewer
                                 A QGIS plugin
 View GCD Files
                             -------------------
        begin                : 2016-07-12
        copyright            : (C) 2016 by NorthArrowResearch
        email                : info@northarrowresearch.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GCDViewer class from file GCDViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gcd_viewer import GCDViewer
    return GCDViewer(iface)
