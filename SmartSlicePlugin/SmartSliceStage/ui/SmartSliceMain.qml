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
import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
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
                

                /* 
                    Smart Slice Button Click Event 
                */
                onClicked: {
                    //  Show Validation Dialog
                    smartSliceValidation.visible = true
                    SmartSlice.Proxy.sendJobSignal()
                    validationSimulator.start()
                }
            }
        }
    }

    Rectangle {
        id: smartSliceValidation
        
        property string validationBlue : "#2671e7"
        
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: UM.Theme.getSize("thick_margin").width
        anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
        
        width: UM.Theme.getSize("action_panel_widget").width
        height: myColumn.height + 2 * UM.Theme.getSize("thick_margin").width
        
        color: UM.Theme.getColor("main_background")
        border.width: UM.Theme.getSize("default_lining").width
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width

        visible: false

        Label {
            id: validationProgress
            text: "Validating requirements..."
            
            anchors.left: parent.left
            anchors.leftMargin: 15
            anchors.top: parent.top
            anchors.topMargin: 10

            font: UM.Theme.getFont("default");

        }

        Label {
            id: validationResultsBad
            text: "Requirements not met!\nOptimize to meet requirements?"
            
            anchors.left: parent.left
            anchors.leftMargin: 15
            anchors.top: parent.top
            anchors.topMargin: 10

            height: parent.height / 2
            width: parent.width

            font: UM.Theme.getFont("default")

            visible: false

            //  Optimize Button
            Rectangle 
            {
                id: validationOptimizeButton

                //  Anchors
                anchors.right: parent.right
                anchors.rightMargin: UM.Theme.getSize("thick_margin").width + 5
                anchors.top: parent.bottom

                //  Sizing
                height: parent.height / 2
                width: parent.width * 3 / 5
                
                //  Styling
                color: smartSliceValidation.validationBlue
                border.width: UM.Theme.getSize("default_lining").width
                border.color: UM.Theme.getColor("lining")

                //  Button Text
                Label {
                    text: "Optimize"
                    anchors.fill: parent; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                    font: UM.Theme.getFont("default"); color: "white"
                
                    MouseArea
                    {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: smartSliceValidation.reset()
                    }
                }
            }

            //  Preview Button
            Rectangle {
                id: validationPreviewButton

                //  Anchors
                anchors.left: parent.left
                anchors.top: parent.bottom

                //  Sizing
                height: parent.height / 2
                width: parent.width / 4
                
                //  Coloring
                color: "#dddddd"

                //  Button Text
                Label {
                    text: "Preview"
                    anchors.fill: parent; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                    font: UM.Theme.getFont("default"); color: smartSliceValidation.validationBlue
                }
            }

        }

        
        /*
            Results Window
        */
        Rectangle {
            id: validationResultsDialog

            //  Anchors
            anchors.bottom: parent.top
            anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
            anchors.right: parent.right
        
            //  Sizing
            width: UM.Theme.getSize("action_panel_widget").width
            height: (myColumn.height + 2 * UM.Theme.getSize("thick_margin").width) * 5 / 2
            
            //  Styling
            color: UM.Theme.getColor("main_background")
            border.width: UM.Theme.getSize("default_lining").width
            border.color: UM.Theme.getColor("lining")
            radius: UM.Theme.getSize("default_radius").width

            visible: false


            /* REQUIREMENTS HEADER */
            Label {
                id: labelReqs
                text: "REQUIREMENTS"

                anchors.left: parent.left; anchors.leftMargin: UM.Theme.getSize("thick_margin").width
                anchors.top: parent.top; anchors.topMargin: UM.Theme.getSize("thick_margin").height
                
                font.pixelSize: 18
                color: smartSliceValidation.validationBlue
            }

            /* OBJECTIVE COLUMN */
            Label {
                id: labelObj
                text: "Objective"

                anchors.left: labelReqs.left; anchors.top: labelReqs.bottom

                width: parent.width / 3

                font.pixelSize: 16
                font.bold: true

                Label {
                    id: labelSafety
                    text: "Factor of Safety:" 

                    anchors.left: parent.left; anchors.top: parent.bottom

                    font.pixelSize: 14
                }

                Label {
                    id: labelDisplace
                    text: "Max Displacement:" 

                    anchors.left: parent.left; anchors.top: labelSafety.bottom

                    font.pixelSize: 14
                }
            }

            /* OBJECTIVE COLUMN */
            Label {
                id: labelComp
                text: "Computed"

                anchors.left: labelObj.right; anchors.top: labelReqs.bottom

                width: parent.width / 3

                font.pixelSize: 16
                font.bold: true

                Label {
                    id: labelSafetyComp
                    text: Data.SafetyFactorComputed()

                    anchors.left: parent.left; anchors.top: parent.bottom

                    font.pixelSize: 14
                }

                Label {
                    id: labelDisplaceComp
                    text: Data.MaxDeflectionComputed()

                    anchors.left: parent.left; anchors.top: labelSafetyComp.bottom

                    font.pixelSize: 14
                }
            }

            /* Target COLUMN */
            Label {
                id: labelTgt
                text: "Target"

                anchors.left: labelComp.right; anchors.top: labelReqs.bottom

                width: parent.width / 3

                font.pixelSize: 16
                font.bold: true

                Label {
                    id: labelSafetyTar
                    text: Data.SafetyFactorTarget()

                    anchors.left: parent.left; anchors.top: parent.bottom

                    font.pixelSize: 14
                }

                Label {
                    id: labelDisplaceTar
                    text: Data.MaxDeflectionTarget()

                    anchors.left: parent.left; anchors.top: labelSafetyTar.bottom

                    font.pixelSize: 14
                }
            }
            

            /* TIME ESTIMATION HEADER */
            Label {
                id: labelTimeEst
                text: "TIME ESTIMATION"

                anchors.left: parent.left; anchors.leftMargin: UM.Theme.getSize("thick_margin").width
                anchors.top: labelObj.bottom; anchors.topMargin: 50
                
                font.pixelSize: 18
                color: smartSliceValidation.validationBlue
            }

            Item {
                id: leftTimeEst
                width: parent.width / 3
                
                anchors.left: labelTimeEst.left; anchors.top: labelTimeEst.bottom

                //  Infill
                Label {
                    id: labelInfills
                    text: "Infills:"

                    anchors.left: parent.left; anchors.top: parent.top

                    font.pixelSize: 14
                }
                //  Inner Walls
                Label {
                    id: labelIWalls
                    text: "Inner Walls:"

                    anchors.left: parent.left; anchors.top: labelInfills.bottom

                    font.pixelSize: 14
                }
                //  Outer Walls
                Label {
                    id: labelOWalls
                    text: "Outer Walls:"

                    anchors.left: parent.left; anchors.top: labelIWalls.bottom

                    font.pixelSize: 14
                }
                //  Retractions
                Label {
                    id: labelRetract
                    text: "Retractions:"

                    anchors.left: parent.left; anchors.top: labelOWalls.bottom

                    font.pixelSize: 14
                }
                //  Skin
                Label {
                    id: labelSkin
                    text: "Skin:"

                    anchors.left: parent.left; anchors.top: labelRetract.bottom

                    font.pixelSize: 14
                }
                //  Skirt
                Label {
                    id: labelSkirt
                    text: "Skirt:"

                    anchors.left: parent.left; anchors.top: labelSkin.bottom

                    font.pixelSize: 14
                }
                //  Travel
                Label {
                    id: labelTravel
                    text: "Travel:"

                    anchors.left: parent.left; anchors.top: labelSkirt.bottom

                    font.pixelSize: 14
                }
            }

            Item {
                id: centerTimeEst
                width: parent.width / 3
                
                anchors.left: labelComp.left; anchors.top: labelTimeEst.bottom

                //  Infill
                Label {
                    id: labelInfillsComp
                    text: Data.InfillsComputed()

                    anchors.left: parent.left; anchors.top: parent.top

                    font.pixelSize: 14
                }
                //  Inner Walls
                Label {
                    id: labelIWallsComp
                    text: Data.InnerWallsComputed()

                    anchors.left: parent.left; anchors.top: labelInfillsComp.bottom

                    font.pixelSize: 14
                }
                //  Outer Walls
                Label {
                    id: labelOWallsComp
                    text: Data.OuterWallsComputed()

                    anchors.left: parent.left; anchors.top: labelIWallsComp.bottom

                    font.pixelSize: 14
                }
                //  Retractions
                Label {
                    id: labelRetractComp
                    text: Data.RetractionsComputed()

                    anchors.left: parent.left; anchors.top: labelOWallsComp.bottom

                    font.pixelSize: 14
                }
                //  Skin
                Label {
                    id: labelSkinComp
                    text: Data.SkinComputed()

                    anchors.left: parent.left; anchors.top: labelRetractComp.bottom

                    font.pixelSize: 14
                }
                //  Skirt
                Label {
                    id: labelSkirtComp
                    text: Data.SkirtComputed()

                    anchors.left: parent.left; anchors.top: labelSkinComp.bottom

                    font.pixelSize: 14
                }
                //  Travel
                Label {
                    id: labelTravelComp
                    text: Data.TravelComputed()

                    anchors.left: parent.left; anchors.top: labelSkirtComp.bottom

                    font.pixelSize: 14
                }
            }

            Item {
                id: rightTimeEst
                width: parent.width / 3
                
                anchors.left: labelTgt.left; anchors.top: labelTimeEst.bottom

                //  Infill
                Label {
                    id: labelInfillsTgt
                    text: Data.InfillsTarget()

                    anchors.left: parent.left; anchors.top: parent.top

                    font.pixelSize: 14
                }
                //  Inner Walls
                Label {
                    id: labelIWallsTgt
                    text: Data.InnerWallsTarget()

                    anchors.left: parent.left; anchors.top: labelInfillsTgt.bottom

                    font.pixelSize: 14
                }
                //  Outer Walls
                Label {
                    id: labelOWallsTgt
                    text: Data.OuterWallsTarget()

                    anchors.left: parent.left; anchors.top: labelIWallsTgt.bottom

                    font.pixelSize: 14
                }
                //  Retractions
                Label {
                    id: labelRetractTgt
                    text: Data.RetractionsTarget()

                    anchors.left: parent.left; anchors.top: labelOWallsTgt.bottom

                    font.pixelSize: 14
                }
                //  Skin
                Label {
                    id: labelSkinTgt
                    text: Data.SkinTarget()

                    anchors.left: parent.left; anchors.top: labelRetractTgt.bottom

                    font.pixelSize: 14
                }
                //  Skirt
                Label {
                    id: labelSkirtTgt
                    text: Data.SkirtTarget()

                    anchors.left: parent.left; anchors.top: labelSkinTgt.bottom

                    font.pixelSize: 14
                }
                //  Travel
                Label {
                    id: labelTravelTgt
                    text: Data.TravelTarget()

                    anchors.left: parent.left; anchors.top: labelSkirtTgt.bottom

                    font.pixelSize: 14
                }
            }
            

            /* Material ESTIMATION HEADER */
            Label {
                id: labelMatEst
                text: "MATERIAL ESTIMATION"

                anchors.left: parent.left; anchors.leftMargin: UM.Theme.getSize("thick_margin").width
                anchors.bottom: parent.bottom; anchors.bottomMargin: UM.Theme.getSize("thick_margin").height + 20

                width: parent.width
                
                font.pixelSize: 18
                color: smartSliceValidation.validationBlue

                Label {
                    id: labelMatEstMat
                    text: Data.Material()

                    anchors.left: parent.left; anchors.top: parent.bottom

                    width: parent.width / 4
                }

                Label {
                    id: labelMatEstLength
                    text: Data.Length()

                    anchors.left: labelMatEstMat.right; anchors.top: parent.bottom

                    width: parent.width / 4
                }

                Label {
                    id: labelMatEstWeight
                    text: Data.Weight()

                    anchors.left: labelMatEstLength.right; anchors.top: parent.bottom

                    width: parent.width / 4
                }

                Label {
                    id: labelMatEstCost
                    text: Data.Cost()

                    anchors.left: labelMatEstWeight.right; anchors.top: parent.bottom

                    width: parent.width / 4
                }
            }
        }

        //  Simulate 5 seconds of validation, then update to show results
        Timer {
            id: validationSimulator
            interval: 5000; running: false; repeat: false
            onTriggered: parent.updateResults()
        }

        function updateResults() 
        {
            validationProgress.visible = false
            validationResultsBad.visible = true
            validationResultsDialog.visible = true
        }

        function reset()
        {
            validationResultsDialog.visible = false
            validationResultsBad.visible = false
            validationProgress.visible = true
            smartSliceValidation.visible = false
        }
    }
}

