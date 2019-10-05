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
        *  Toolbox Sidebar (Middle Left)


    Table of Contents
    =================
    1.) Brand Logo
    2.) Smart Slice Button Window
    3.) Smart Slice Sidebar Widget 
      3.a) Constraints 
        3.a.1) Constraints Button
        3.a.2) Constraints Dialog
      3.b) Requirements
        3.b.1) Requirements Button
        3.b.2) Requirements Dialog
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

  /*
      2.) Smart Slice Button Window
  */
  Rectangle {
    id: smartSliceWindow //  TODO: Change to Widget when everything works
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.rightMargin: UM.Theme.getSize("thick_margin").width
    anchors.bottomMargin: UM.Theme.getSize("thick_margin").height

    border.color: "grey"

    width: 325 
    height: 63
    radius: 5


    Rectangle
    {
      id: smartSliceButton
      anchors.fill: parent
      anchors.leftMargin: 10
      anchors.rightMargin: 10
      anchors.topMargin: 10
      anchors.bottomMargin: 10

      //  Becomes "Active" after at minimum, 1 load and 1 anchor has been set
      property bool isActive: (smartSliceMain.smartLoads > 0 && smartSliceMain.smartAnchors > 0) ? true : false
      property string grayInactive: "#c0c0c0"
      property string grayActive: "#cccccc"
      property string blueInactive: "#2222ff"
      property string blueActive: "#3333ff"


      color: (isActive) ? blueInactive : grayInactive

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
      }   
      

      MouseArea {
        anchors.fill: parent
        hoverEnabled: true         //this line will enable mouseArea.containsMouse
        onEntered: { if (parent.isActive) {parent.color = parent.blueActive} else {parent.color = parent.grayActive} }
        onExited:  { if (parent.isActive) {parent.color = parent.blueInactive} else {parent.color = parent.grayInactive} }
      }
    }
  }

  /*
    3.) Smart Slice Sidebar Widget 
  */
  Rectangle {
    id: smartSliceSidebar
    anchors.left: parent.left
    anchors.bottom: parent.verticalCenter
    anchors.bottomMargin: 100

    border.width: 1
    border.color: "black"

    height: 100
    width: 51

    

    /*
      Requirements Requirements Button
    */
    Rectangle {
      id: buttonRequirements
      anchors.left: parent.left
      anchors.leftMargin: 3
      anchors.bottom: parent.bottom
      anchors.bottomMargin: 3
      height: 45
      width: 45

      border.color: "grey"
      border.width: 2
      color: (dialogRequirements.inFocus) ? "#ccccff" : "white"

      //  Requirements Dialog
      Rectangle
      {
        id: dialogRequirements
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.right
        anchors.leftMargin: 25
        height: 60
        width: 200
        radius: 5

        border.width: 1
        border.color: "#cccccc"

        visible: false
        property bool inFocus: false
        
        //  Safety Factor Text/Text Field
        Text {
          id: textSafetyFactor
          anchors.top: parent.top
          anchors.topMargin: 8
          anchors.left: parent.left
          anchors.leftMargin: 20

          font.pixelSize: 20
          font.bold: true
        
          text: "Factor of Safety  \u2265"

          TextField {
            id: valueSafetyFactor
            anchors.left: parent.right
            anchors.leftMargin: 10

            width: 40
            height: 20

            placeholderText: ""
          }
        }
        
        //  Max Deflection Text/Text Field
        Text {
          id: textMaxDeflect
          anchors.top: parent.top
          anchors.topMargin: 30
          anchors.left: parent.left
          anchors.leftMargin: 20

          font.pixelSize: 20
          font.bold: true
        
          text: "Max Deflection  \u2264"

          TextField {
            id: valueMaxDeflect
            anchors.left: parent.right
            anchors.leftMargin: 10

            width: 40
            height: 20

            placeholderText: "mm"
          }
        }
      }
      
      //  Requirements Hover Field
      MouseArea {
        anchors.fill: parent
        hoverEnabled: true         //this line will enable mouseArea.containsMouse
        onClicked: { if (dialogRequirements.inFocus) {dialogRequirements.inFocus = false} else {dialogRequirements.inFocus = true} }
        onEntered: { dialogRequirements.visible = true }
        onExited:  { if (dialogRequirements.inFocus == true) {} else {dialogRequirements.visible = false } }
      }
    }
  }
}    

