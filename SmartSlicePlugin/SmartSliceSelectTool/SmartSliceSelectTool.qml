/*
  dialogConstraints.qml
  Teton Simulation
  Authored on   October 5, 2019
  Last Modified October 5, 2019
*/

/*
  Contains structural definitions for Constraints UI Dialog
*/


//  API Imports
import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura

/*
  Constraints
*/
Item {
    id: constraintsTooltip
    width: childrenRect.width
    height: childrenRect.height
    
    UM.I18nCatalog {
        id: catalog;
        name: "smartslice"
    }
    
    Component.onCompleted: {
        selectAnchorButton.checked = UM.ActiveTool.properties.getValue("AnchorSelectionActive")
        selectLoadButton.checked = UM.ActiveTool.properties.getValue("LoadSelectionActive")
    }
      
    Button
    {
        id: selectAnchorButton
        
        anchors.left: parent.left
        z: 2
    
        text: catalog.i18nc("@action:button", "Anchor (Mount)")
        iconSource: "./anchor_icon.svg"
        property bool needBorder: true

        style: UM.Theme.styles.tool_button;

        onClicked: {
            UM.ActiveTool.triggerAction("setAnchorSelection");
            selectAnchorButton.checked = true;
            selectLoadButton.checked = false;
        }
        //checked: constraintsRoot.anchorActive
    }

    Button
    {
        id: selectLoadButton
        anchors.left: selectAnchorButton.right;
        anchors.leftMargin: UM.Theme.getSize("default_margin").width;
        z: 1
        
        text: catalog.i18nc("@action:button", "Load (Directed force)")
        iconSource: "./load_icon.svg"
        property bool needBorder: true

        style: UM.Theme.styles.tool_button;

        onClicked: {
            UM.ActiveTool.triggerAction("setLoadSelection");
            selectAnchorButton.checked = false;
            selectLoadButton.checked = true;
        }
        //checked: constraintsRoot.loadActive
    }
}
