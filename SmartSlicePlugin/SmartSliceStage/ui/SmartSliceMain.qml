/*
    SmartSliceMain.qml
    Teton Simulation
    Last Modified October 3, 2019
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
      TODO: Migrate components to Action Widgets
  */
  Cura.ActionPanelWidget
  {
    id: smartSliceWidget
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.rightMargin: UM.Theme.getSize("thick_margin").width
    anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
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
  
  /*
    3.) Smart Slice Sidebar Widget 
  */
  Rectangle {
    id: smartSliceSidebarButtons
    anchors.left: parent.left
    anchors.top: parent.verticalCenter
    anchors.leftMargin: UM.Theme.getSize("thick_margin").width
    anchors.topMargin: UM.Theme.getSize("thick_margin").height

    border.width: 1
    border.color: "black"

    height: 100
    width: 50


    /*
      3.a) Constraints
    */

    /*
      3.a.1) Constraints Button
    */
    Rectangle {
      id: buttonConstraints
      anchors.left: parent.left
      anchors.leftMargin: 2.5
      anchors.top: parent.top
      anchors.topMargin: 2.5
      height: 45
      width: 45
      color: (dialogConstraints.inFocus) ? "green" : "blue"

      /*
        3.a.2) Constraints Dialog
      */
      Rectangle
      {
        id: dialogConstraints
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.right
        anchors.leftMargin: 25
        height: 135
        width: 125
        radius: 5

        border.width: 1
        border.color: "#cccccc"

        visible: false
        property bool inFocus: false

        //  Header Text
        Text {
          text: "Structural"
          anchors.top: parent.top
          anchors.topMargin: 4
          anchors.left: parent.left
          anchors.leftMargin: 10
          font.bold: true
          font.pixelSize: 22
        }

        //  Seperator
        Rectangle { anchors.right: parent.right; anchors.top: parent.top; anchors.topMargin: 27; height: 2; width: 100; color: "#cccccc" }
        
        //  Subheader Text
        Text {
          text: "Mounting"
          anchors.top: parent.top
          anchors.topMargin: 30
          anchors.left: parent.left
          anchors.leftMargin: 15
          font.bold: true
          font.pixelSize: 18
        }

        //  "Anchors" Text
        Text {
          text: "Anchors"
          anchors.top: parent.top
          anchors.topMargin: 52
          anchors.left: parent.left
          anchors.leftMargin: 35
          font.pixelSize: 18

          
          //  "Mount Text"
          Text {
            text: "Mount"
            anchors.top: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 15
            font.pixelSize: 17
          }     
        } 

        //  Anchors Collapse Arrow
        Image {
          anchors.top: parent.top
          anchors.topMargin: 54
          anchors.left: parent.left
          anchors.leftMargin: 15

          width: 12
          fillMode: Image.PreserveAspectFit
          source: "../images/collapse.png"
        }

        //  "Loads" Text
        Text {
          text: "Loads"
          anchors.top: parent.top
          anchors.topMargin: 90
          anchors.left: parent.left
          anchors.leftMargin: 35
          font.pixelSize: 18
        
          //  "Push" Text
          Text {
            text: "Push"
            anchors.top: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 15
            font.pixelSize: 17
          }       
        }        

        //  Anchors Collapse Arrow
        Image {
          anchors.top: parent.top
          anchors.topMargin: 90
          anchors.left: parent.left
          anchors.leftMargin: 15

          width: 12
          fillMode: Image.PreserveAspectFit
          source: "../images/collapse.png"

          //  Collapsed option
          property bool collapsed: false

          MouseArea {
            anchors.fill: parent
            hoverEnabled: true         //this line will enable mouseArea.containsMouse
            onClicked: { 
              if (parent.collapsed) 
              {
                parent.collapsed = false
              } else {
                parent.collapsed = true
              } 
            }
          }
        }
      }
      
      //  Constraints Hover Field
      MouseArea {
        anchors.fill: parent
        hoverEnabled: true         //this line will enable mouseArea.containsMouse
        onClicked: { if (dialogConstraints.inFocus) {dialogConstraints.inFocus = false} else {dialogConstraints.inFocus = true} }
        onEntered: { dialogConstraints.visible = true }
        onExited:  { if (dialogConstraints.inFocus == true) {} else {dialogConstraints.visible = false } }
      }
    }
    

    /*
      Requirements Requirements Button
    */
    Rectangle {
      id: buttonRequirements
      anchors.left: parent.left
      anchors.leftMargin: 2.5
      anchors.bottom: parent.bottom
      anchors.bottomMargin: 2.5
      height: 45
      width: 45
      color: (dialogRequirements.inFocus) ? "green" : "blue"

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

