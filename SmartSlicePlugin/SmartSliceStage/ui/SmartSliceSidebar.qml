/*
  SmartSliceSidebar.qml
  Teton Simulation, Inc
  Authored on   October 2, 2019
  Last Modified October 2, 2019
*/

/*
  Contains structural definitions for Smart Slice sidebar toolbox

  This toolbox appears on the middle left side of the screen while in 
    Smart Slice user environment (Stage).  

  The toolbox includes:
    * Adding/Editing Use Case Constraints
    * Adding/Editing Requirements
*/


//  Standard Imports
import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice


/*
  Side Bar Definition
*/
Item {
  id: smartSliceSidebar

  Rectangle {
    id: smartSliceSidebarButtons
    anchors.left: parent.left
    anchors.top: parent.top
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
    /*Rectangle {
      id: buttonConstraints

      anchors.left: parent.left
      anchors.top: parent.top

      height: 45
      width: 45
      color: "blue"
    }

    /*
      Requirements Requirements Button
    */
    /*Rectangle {
      id: buttonRequirements

      anchors.left: parent.left
      anchors.bottom: parent.bottom

      height: 45
      width: 45
      color: "blue"
    }*/
    
  }
}

