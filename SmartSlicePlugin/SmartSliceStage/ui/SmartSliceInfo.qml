import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura

import SmartSlice 1.0 as SmartSlice
import "Bridge.js" as Data

RowLayout {
    id: smartSlicePopupContents

    property string validationBlue : "#2671e7"

    width: UM.Theme.getSize("action_panel_widget").width
    height: myColumn.height + 2 * UM.Theme.getSize("thick_margin").width

    anchors.fill: parent

    /* REQUIREMENTS HEADER */
    Label {
        id: labelReqs

        anchors.left: parent.left
        anchors.leftMargin: UM.Theme.getSize("thick_margin").width
        anchors.top: parent.top
        anchors.topMargin: UM.Theme.getSize("thick_margin").height

        font.pixelSize: 18
        color: smartSlicePopupContents.validationBlue

        text: "REQUIREMENTS"
    }

    /* OBJECTIVE COLUMN */
    Label {
        id: labelObj
        text: "Objective"

        anchors.left: labelReqs.left
        anchors.top: labelReqs.bottom

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
            text: "50"

            anchors.left: parent.left
            anchors.top: parent.bottom

            font.pixelSize: 14
        }

        Label {
            id: labelDisplaceComp
            text: Data.MaxDeflectionComputed()

            anchors.left: parent.left
            anchors.top: labelSafetyComp.bottom

            font.pixelSize: 14
        }
    }

    /* Target COLUMN */
    Label {
        id: labelTgt
        text: "Target"

        anchors.left: labelComp.right
        anchors.top: labelReqs.bottom

        width: parent.width / 3

        font.pixelSize: 16
        font.bold: true

        Label {
            id: labelSafetyTar
            text: SmartSlice.Variables.safetyFactor

            anchors.left: parent.left
            anchors.top: parent.bottom

            font.pixelSize: 14
        }

        Label {
            id: labelDisplaceTar
            text: SmartSlice.Variables.maxDeflect

            anchors.left: parent.left
            anchors.top: labelSafetyTar.bottom

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
        color: smartSlicePopupContents.validationBlue
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
            text: "2.5"

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
        color: smartSlicePopupContents.validationBlue

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
