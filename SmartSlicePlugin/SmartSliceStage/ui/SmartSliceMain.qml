import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice

Item {
    id: smartSliceMain


    Image {
        id: tetonBranding 
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.leftMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height

        width: 250
        fillMode: Image.PreserveAspectFit
        source: "../images/horizontal.png"
        mipmap: true
    }

    Cura.ActionPanelWidget
    {
        id: smartSliceWidget
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
    }

    /*
        Smart Slice Main Widget Window
    */
    Rectangle {
        id: smartSliceWindow //  TODO: Change to Widget when everything works
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height

        border.width: 1
        border.color: "black"

        width: 200 
        height: 60
        radius: 5

        Rectangle
        {
            id: smartSliceButtonInactive
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 10
            anchors.bottomMargin: 10

            
            color: "#bbbbbb"
            width: 180
            height: 40
            radius: 5

            Text {
                text: "Smart Slice"
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                width: parent.width
                height: parent.height

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true         //this line will enable mouseArea.containsMouse
                    onEntered: { parent.parent.color = "#cccccc" }
                    onExited:  { parent.parent.color = "#c2c2c2"}
                }
            }
            
        }

    }

    
}

