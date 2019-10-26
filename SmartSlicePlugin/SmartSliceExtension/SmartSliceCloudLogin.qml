import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Window 2.1

import UM 1.1 as UM

import SmartSlice 1.0 as SmartSlice

UM.Dialog
{
    title: catalog.i18nc("@title:window", "Cloud login")

    width: Math.floor(screenScaleFactor * 400);
    minimumWidth: width;
    maximumWidth: width;

    height: Math.floor(screenScaleFactor * 350);
    minimumHeight: height;
    maximumHeight: height;

    onVisibilityChanged:
    {
        if (visible)
        {
            //installationsDropdown.updateCurrentIndex();
            //showWizardCheckBox.checked = manager.getBoolValue("show_export_settings_always");
        }
    }

    ColumnLayout {
        UM.I18nCatalog{id: catalog; name: "smartslice"}
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width

        spacing: UM.Theme.getSize("default_margin").height

        property Item showWizard
        property Item autoRotateCheckBox
        property Item qualityDropdown
        //property Item choiceModel
        property Item installationsDropdown

        Column {
            Layout.alignment: Qt.AlignCenter
            Image {
                width: Math.floor(screenScaleFactor * 300);
                
                fillMode: Image.PreserveAspectFit
                source: "images/branding.png"
                mipmap: true
            }
        }
        
        Text {
            id: statusText
            
            Layout.alignment: Qt.AlignCenter
            
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            
            text: SmartSlice.Cloud.loginStatus
        }
        
        TextField {
            id: username_input
            
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
            //Layout.preferredWidth: 300
            
            font: UM.Theme.getFont("default")
            
            text: SmartSlice.Cloud.loginName
            onTextChanged: {
                SmartSlice.Cloud.loginName = text
            }
            
            onAccepted: password_input.forceActiveFocus()
            placeholderText: catalog.i18nc("@label", "Username")
            KeyNavigation.tab: password_input
        }

        TextField {
            id: password_input
            
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
            
            font: UM.Theme.getFont("default")
            
            text: SmartSlice.Cloud.loginPassword
            onTextChanged: {
                SmartSlice.Cloud.loginPassword = text
            }
            
            //onAccepted: login()
            placeholderText: catalog.i18nc("@label", "Password")
            echoMode: TextInput.Password
            KeyNavigation.tab: login_button
        }
        
        Button
        {
            id: login_button
            
            Layout.alignment: Qt.AlignCenter

            text: catalog.i18nc("@action:button", "Login")
            onClicked:
            {
                if(SmartSlice.Cloud.loginResult) {
                    close();
                } else {
                    SmartSlice.Cloud.loginStatus = catalog.i18nc("@action:button", "Login failed! Please try again!")
                }
            }
            enabled: true
            
            KeyNavigation.tab: username_input
        }
    }
}