/*
    SmartSliceMain.qml
    Teton Simulation
    Last Modified October 16, 2019
*/

/*
    Contains definitions for Smart Slice's main structural UI elements

    This includes: (Vert. Horiz.)
        *  Brand Logo (Bottom Middle)
        *  "Smart Slice" Button (Bottom Right)
*/


//  API Imports
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice

import "Bridge.js" as Data

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
        source: "../images/branding.png"
        mipmap: true
    }

    //  2.) Smart Slice Window
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
                    // Main status message 
                    Label {
                    
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        font: UM.Theme.getFont("default");
                        renderType: Text.NativeRendering
            
                        text: catalog.i18nc("@action:button", "<Status name>")
            
                    }
                    
                    // Secondary status message with hint
                    Label {
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        font: UM.Theme.getFont("default")
                        renderType: Text.NativeRendering
            
                        text: catalog.i18nc("@action:button", "<Status hint>")
            
                    }
                }
                
                // Status indicator
                UM.RecolorImage {
                    id: smartSliceInfoIcon
                    source: UM.Theme.getIcon("info")

                    Layout.alignment: Qt.AlignTop

                    width: UM.Theme.getSize("section_icon").width
                    height: UM.Theme.getSize("section_icon").height
                
                    color: UM.Theme.getColor("icon")
                
                    MouseArea
                    {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: smartSlicePopup.open()
                        onExited: smartSlicePopup.close()
                    }
                
                    // Popup message with slice results
                    Popup {
                        id: smartSlicePopup

                        y: -(height + UM.Theme.getSize("default_arrow").height + UM.Theme.getSize("thin_margin").height)
                        x: parent.width - width + UM.Theme.getSize("thin_margin").width

                        width: UM.Theme.getSize("action_panel_widget").width
                        height: myColumn.height + 2 * UM.Theme.getSize("thick_margin").width

                        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
                
                        opacity: opened ? 1 : 0
                        Behavior on opacity { NumberAnimation { duration: 100 } }
                
                        Loader {
                            source: "SmartSliceInfo.qml";
                        }
                
                        background: UM.PointingRectangle
                        {
                            color: UM.Theme.getColor("tool_panel_background")
                            borderColor: UM.Theme.getColor("lining")
                            borderWidth: UM.Theme.getSize("default_lining").width
                
                            target: Qt.point(width - (smartSliceInfoIcon.width / 2) - UM.Theme.getSize("thin_margin").width,
                                            height + UM.Theme.getSize("default_arrow").height - UM.Theme.getSize("thin_margin").height)
                
                            arrowSize: UM.Theme.getSize("default_arrow").width
                        }
                    }
                }
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
                

                /* 
                    Smart Slice Button Click Event 
                */
                onClicked: {
                    //  Show Validation Dialog
                    SmartSlice.Proxy.sendJobSignal()
                    validationSimulator.start()
                }
            }
        }
    }
}

