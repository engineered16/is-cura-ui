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
import SmartSlice 1.0 as SmartSlice



/*
  Constraints
*/
Item {
    /*
      Constraints Dialog
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

      //  Dialog Header Text
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
      

      //  Anchors Collapse Arrow
      Image {
        anchors.top: parent.top
        anchors.topMargin: 54
        anchors.left: parent.left
        anchors.leftMargin: 15

        width: 12
        fillMode: Image.PreserveAspectFit
        source: "assets/collapse.png"
      }
      
      //  Category Text 
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

        
        /*
          Mount Tool
        */

        //  Mount Tool Text
        Text {
          text: "Mount"
          anchors.top: parent.bottom
          anchors.left: parent.left
          anchors.leftMargin: 15
          font.pixelSize: 17

          //  Mount Tool Button
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
            
            //  Mouse Cursor Icon
            Image{
              source: "assets/cursor_white_small.png"
              anchors.fill: parent
              anchors.topMargin: 2
              anchors.bottomMargin: 2
              anchors.leftMargin: 2
              anchors.rightMargin: 2
                    
              //  Click/Hover Events
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
}
