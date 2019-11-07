/*
  SmartSliceLoadDialog.qml
  Teton Simulation
  Authored on   November 6, 2019
  Last Modified November 6, 2019
*/


Item {
    id: applyLoadDialog

    UM.I18nCatalog {
        id: catalog
        name: "smartslice"
    }


    //  Default Traits
    Rectangle {
        id: loadPopup

        width: UM.Theme.getSize("action_panel_widget").width
        height: 100 + 2 * UM.Theme.getSize("thick_margin").width

        anchors.left: parent.parent.left
        anchors.bottom: parent.parent.bottom
        anchors.leftMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height

        color: UM.Theme.getColor("main_background")
        border.width: UM.Theme.getSize("default_lining").width
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width
    }


}

