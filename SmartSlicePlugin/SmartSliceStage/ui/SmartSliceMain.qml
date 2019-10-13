/*
    SmartSliceMain.qml
    Teton Simulation
    Last Modified October 5, 2019
*/

/*
    Contains definitions for Smart Slice's main structural UI elements

    This includes: (Vert. Horiz.)
        *  Brand Logo (Bottom Middle)
        *  "Smart Slice" Button (Bottom Right)
*/


//  API Imports
import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice


//  Main UI Stage Components
Item {
    id: smartSliceMain

    //  Main Stage Accessible Properties
    property int smartLoads : 0
    property int smartAnchors : 0

    //  1.) Brand Logo
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

    //  2.) Smart Slice Button Window
    Rectangle {
        id: smartSliceWindow //    TODO: Change to Widget when everything works
        
        width: UM.Theme.getSize("action_panel_widget").width
        height: myColumn.height + 2 * UM.Theme.getSize("thick_margin").width
        
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
        
        color: UM.Theme.getColor("main_background")
        border.width: UM.Theme.getSize("default_lining").width
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width


        ColumnLayout {
            id: myColumn
            
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: UM.Theme.getSize("thick_margin").width
            
            RowLayout {
                Layout.fillHeight: true
                Layout.fillWidth: true
                
                ColumnLayout {
                    Layout.fillWidth: true
                    Label {
                        Layout.fillHeight: true
                        font: UM.Theme.getFont("default");
                        renderType: Text.NativeRendering
            
                        text: catalog.i18nc("@action:button", "<Status name>")
            
                    }
                    Label {
                        Layout.fillHeight: true
                        font: UM.Theme.getFont("default");
                        renderType: Text.NativeRendering
            
                        text: catalog.i18nc("@action:button", "<Status hint>")
            
                    }
                }
                
                /*
                UM.RecolorImage {
                    id: widget
                
                    source: UM.Theme.getIcon("info")
                    width: UM.Theme.getSize("section_icon").width
                    height: UM.Theme.getSize("section_icon").height
                
                    color: UM.Theme.getColor("icon")
                
                    MouseArea
                    {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: popup.open()
                        onExited: popup.close()
                    }
                
                    Popup
                    {
                        id: popup
                
                        y: -(height + UM.Theme.getSize("default_arrow").height + UM.Theme.getSize("thin_margin").height)
                        x: parent.width - width + UM.Theme.getSize("thin_margin").width
                
                        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
                
                        opacity: opened ? 1 : 0
                        Behavior on opacity { NumberAnimation { duration: 100 } }
                
                        contentWidth: printJobInformation.width
                        contentHeight: printJobInformation.implicitHeight
                
                        contentItem:
                        {
                            id: printJobInformation
                            width: UM.Theme.getSize("action_panel_information_widget").width
                            
                            Label {
                                text: "Your contents here."
                            }
                        }
                
                        background: UM.PointingRectangle
                        {
                            color: UM.Theme.getColor("tool_panel_background")
                            borderColor: UM.Theme.getColor("lining")
                            borderWidth: UM.Theme.getSize("default_lining").width
                
                            target: Qt.point(width - (widget.width / 2) - UM.Theme.getSize("thin_margin").width,
                                            height + UM.Theme.getSize("default_arrow").height - UM.Theme.getSize("thin_margin").height)
                
                            arrowSize: UM.Theme.getSize("default_arrow").width
                        }
                    }
                }
                */
            }
            Cura.PrimaryButton
            {
            
                id: smartSliceButton
                Layout.fillWidth: true
    
                height: UM.Theme.getSize("action_button").height
    
                text: "Smart Slice"
                
                enabled: SmartSlice.Proxy.hasSliceableNodes

                Connections {
                    target: SmartSlice.Proxy
                    onSliceableNodesChanged: {
                        smartSliceButton.enabled = SmartSlice.Proxy.hasSliceableNodes
                    }
                }
                
                onClicked: {
                    SmartSlice.Proxy.sendJobSignal()
                }
            }
        }
    }
}

