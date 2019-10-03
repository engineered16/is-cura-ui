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

  //  Brand Logo
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

    /* INACTIVE Smart Slice Button */
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
      Smart Slice Sidebar Widget 
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
      Dialogue Layout (1-COLUMN GRID LAYOUT)
    */

    /*
      Use Case Constraints Button
    */
    Rectangle {
      id: buttonConstraints
      anchors.left: parent.left
      anchors.leftMargin: 2.5
      anchors.top: parent.top
      anchors.topMargin: 2.5
      height: 45
      width: 45
      color: "blue"

      //  Constraints Dialog
      Rectangle
      {
        id: dialogConstraints
        anchors.bottom: parent.verticalCenter
        anchors.left: parent.right
        anchors.leftMargin: 25
        height: 100
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
        } 

        //  Anchors Collapse Arrow
        Image {
          anchors.top: parent.top
          anchors.topMargin: 52
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
          anchors.topMargin: 70
          anchors.left: parent.left
          anchors.leftMargin: 35
          font.pixelSize: 18
        }        
        

        //  Anchors Collapse Arrow
        Image {
          anchors.top: parent.top
          anchors.topMargin: 70
          anchors.left: parent.left
          anchors.leftMargin: 15

          width: 12
          fillMode: Image.PreserveAspectFit
          source: "../images/collapse.png"
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
      color: "blue"

      //  Requirements Dialog
      Rectangle
      {
        id: dialogRequirements
        anchors.bottom: parent.verticalCenter
        anchors.left: parent.right
        anchors.leftMargin: 25
        height: 125
        width: 175
        radius: 5

        border.width: 1
        border.color: "#cccccc"

        visible: false
      }
      
      //  Requirements Hover Field
      MouseArea {
        anchors.fill: parent
        hoverEnabled: true         //this line will enable mouseArea.containsMouse
        onEntered: { dialogRequirements.visible = true }
        onExited:  { dialogRequirements.visible = false }
      }
    }
  }
}    

