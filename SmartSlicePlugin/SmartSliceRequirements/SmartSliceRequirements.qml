/*
  dialogRequirements.qml
  Teton Simulation
  Authored on   October 8, 2019
  Last Modified October 8, 2019
*/

/*
  Contains structural definitions for Requirements UI Dialog
*/


// API Imports
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
Item
{
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "smartslice"}

    Grid
    {
        id: textfields;

        anchors.top: parent.top;

        columns: 2;
        flow: Grid.TopToBottom;
        spacing: Math.round(UM.Theme.getSize("default_margin").width / 2);

        // Safety Factor Text/Text Field
        Label {
            height: UM.Theme.getSize("setting_control").height;

            font: UM.Theme.getFont("default");
            renderType: Text.NativeRendering

            text: catalog.i18nc("@action:button", "Factor of Safety \u2265")
        }

        Label {
            height: UM.Theme.getSize("setting_control").height;

            font: UM.Theme.getFont("default");
            renderType: Text.NativeRendering

            text: catalog.i18nc("@action:button", "Max Deflection  \u2264")
        }

        TextField {
            id: valueSafetyFactor
            width: UM.Theme.getSize("setting_control").width;
            height: UM.Theme.getSize("setting_control").height;
            style: UM.Theme.styles.text_field;
            validator: DoubleValidator
            {
                bottom: 1.0  // Every value below this makes scientifically no sense
                decimals: 4
                locale: "en_US"
            }
            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                SmartSlice.Variables.safetyFactor = modified_text; // Will be converted from string to the target data type via SmartSliceVariables
            }

            text: SmartSlice.Variables.safetyFactor
            placeholderText: catalog.i18nc("@action:button", "Must be above 1")
            property string unit: "[1]";
        }

        TextField {
            id: valueMaxDeflect
            width: UM.Theme.getSize("setting_control").width;
            height: UM.Theme.getSize("setting_control").height;
            style: UM.Theme.styles.text_field;
            validator: DoubleValidator
            {
                bottom: 0.1  // Setting lowest value here
                decimals: 4
                locale: "en_US"
            }
            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                SmartSlice.Variables.maxDeflect = modified_text; // Will be converted from string to the target data type via SmartSliceVariables
            }

            text: SmartSlice.Variables.maxDeflect
            placeholderText: ""
            property string unit: "[mm]";
        }

    }
}
