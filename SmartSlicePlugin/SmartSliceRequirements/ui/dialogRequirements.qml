/*
  dialogRequirements.qml
  Teton Simulation
  Authored on   October 8, 2019
  Last Modified October 8, 2019
*/

/*
  Contains structural definitions for Requirements UI Dialog
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
  Requirements
*/
Item {
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
