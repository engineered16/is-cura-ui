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
}    

