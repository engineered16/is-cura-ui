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
    id: smartSliceSidebarButtons
    anchors.left: parent.left
    anchors.bottom: parent.verticalCenter
    anchors.bottomMargin: 100

    border.width: 1
    border.color: "black"

    height: 100
    width: 51


    /*
      3.a) Constraints
    */

    /*
      3.a.1) Constraints Button
    */
    Rectangle {
      id: buttonConstraints
      anchors.left: parent.left
      anchors.leftMargin: 3
      anchors.top: parent.top
      anchors.topMargin: 3
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
        property string activeTool: ""

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

            Rectangle
            {
              id: mountToolButton
              anchors.left: parent.right
              anchors.leftMargin: 10

              width: 17
              height: 17
              property bool toolActive: false

              border.width: (toolActive) ? 1 : 0
              border.color: "blue"
              
              //  Icon
              Image{
                source: "assets/cursor_white_small.png"
                anchors.fill: parent
                anchors.topMargin: 2
                anchors.bottomMargin: 2
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                      
                MouseArea {
                  anchors.fill: parent
                  hoverEnabled: true         //this line will enable mouseArea.containsMouse
                  onClicked: { 
                    smartSliceMain.smartAnchors += 1
                    smartSliceButton.isActive = (smartSliceMain.smartLoads > 0 && smartSliceMain.smartAnchors > 0) ? true : false 
                    smartSliceButton.color = (smartSliceButton.isActive) ? smartSliceButton.blueInactive : smartSliceButton.grayInactive
                    if (mountToolButton.toolActive) 
                    {
                      mountToolButton.toolActive = false 
                      dialogConstraints.activeTool = ""
                    } 
                    else 
                    {
                      mountToolButton.toolActive = true
                      dialogConstraints.activeTool = "mount"
                    }
                    if (dialogConstraints.activeTool = "push") {pushToolButton.toolActive = false}
                  }
                }
              }
            }
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

            Rectangle
            {
              id: pushToolButton
              anchors.left: parent.right
              anchors.leftMargin: 10
              width: 17
              height: 17
              property bool toolActive: false

              border.width: (toolActive) ? 1 : 0
              border.color: "blue"
              
              //  Icon
              Image{
                source: "assets/cursor_white_small.png"
                anchors.fill: parent
                anchors.topMargin: 2
                anchors.bottomMargin: 2
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                      
                MouseArea {
                  anchors.fill: parent
                  hoverEnabled: true         //this line will enable mouseArea.containsMouse
                  onClicked: { 
                    smartSliceMain.smartLoads += 1
                    smartSliceButton.isActive = (smartSliceMain.smartLoads > 0 && smartSliceMain.smartAnchors > 0) ? true : false   
                    smartSliceButton.color = (smartSliceButton.isActive) ? smartSliceButton.blueInactive : smartSliceButton.grayInactive
                    if (pushToolButton.toolActive) 
                    {
                      pushToolButton.toolActive = false 
                      dialogConstraints.activeTool = ""
                    } 
                    else 
                    {
                      pushToolButton.toolActive = true
                      dialogConstraints.activeTool = "push"
                    }
                    if (dialogConstraints.activeTool = "mount") {mountToolButton.toolActive = false}
                  }
                }
              }
            }
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
      anchors.leftMargin: 3
      anchors.bottom: parent.bottom
      anchors.bottomMargin: 3
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

