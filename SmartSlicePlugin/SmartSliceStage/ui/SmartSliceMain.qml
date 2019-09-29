import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice

Item
{
    id: smartSliceMain

    Cura.ActionPanelWidget
    {
        id: smartSliceWidget
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
    }

/*
    Cura.Toolbar
    {
        id: smartSliceToolbar
        
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        
        model: SmartSlice.ToolModel
    }
*/
}

