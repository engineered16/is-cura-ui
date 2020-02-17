/*
    SmartSliceConfirmationPrompt.qml
    Teton Simulation
*/

/*
    Contains structural definitions for Smart Slice's confirmation/cancellation prompt

    This prompt is raised when a user makes a change that would: 
      * Invalidate current set of validation/optimization results
      * Cancel a current validation/optimization attempt
*/

//  API Imports
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.1

import UM 1.2 as UM
import Cura 1.0 as Cura
import SmartSlice 1.0 as SmartSlice


//  Confirm Changes Components
Item {
    id: smartSliceConfirmDialog

    /*
        CONFIRMATION PROMPTS
    */
    Rectangle {
        id: smartSliceConfirm

        width: UM.Theme.getSize("action_panel_widget").width
        height: myColumn.height + 2 * UM.Theme.getSize("thick_margin").width

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter

        color: UM.Theme.getColor("main_background")
        border.width: UM.Theme.getSize("default_lining").width
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width

        visible: SmartSlice.Cloud.confirmationWindowEnabled

        Connections {
            target: SmartSlice.Cloud
            onConfirmationWindowEnabledChanged: { smartSliceConfirm.visible = SmartSlice.Cloud.confirmationWindowEnabled }
            onConfirmationWindowTextChanged: { smartSliceConfirmText.text = SmartSlice.Cloud.confirmationWindowText }
        }

        Label {
            id: smartSliceConfirmText
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: UM.Theme.getSize("thick_margin").width
            text: SmartSlice.Cloud.confirmationWindowText
        }
        
        Cura.PrimaryButton {
            id: smartSliceConfirmContinue

            anchors.bottom: parent.bottom
            anchors.right: parent.right

            anchors.bottomMargin: UM.Theme.getSize("thick_margin").height
            anchors.rightMargin: UM.Theme.getSize("thick_margin").width

            enabled: true
            text: "Continue"

            /*
                Re-optimize Continue Button Click Event
            */
            onClicked: {
                //  Show Validation Dialog
                //  TODO: Generalize this reoptimize cancellation for validation as well
                SmartSlice.Cloud.confirmationConfirmClicked()
            }
        }

        Cura.SecondaryButton {
            id: smartSliceConfirmCancel

            anchors.right: smartSliceConfirmContinue.left
            anchors.bottom: parent.bottom

            anchors.rightMargin: UM.Theme.getSize("thick_margin").width
            anchors.bottomMargin: UM.Theme.getSize("thick_margin").height

            enabled: true
            text: "Cancel"

            /*
                Re-optimize Cancel Button Click Event
            */
            onClicked: {
                //  Show Validation Dialog
                //  TODO: Generalize this reoptimize cancellation for validation as well
                SmartSlice.Cloud.confirmationCancelClicked()
            }
        }
    }
}
