import QtQuick 2.7
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

import UM 1.2 as UM
import SmartSlice 1.0 as SmartSlice

UM.Dialog {
    id: aboutDialog
    title: "Smart Slice by Teton Simulation"

    width: Math.floor(screenScaleFactor * 400);
    minimumWidth: width;
    maximumWidth: width;

    height: Math.floor(screenScaleFactor * 350);
    minimumHeight: height;
    maximumHeight: height;

    ColumnLayout {
        UM.I18nCatalog{id: catalog; name: "smartslice"}
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width

        spacing: UM.Theme.getSize("default_margin").height

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
            Layout.alignment: Qt.AlignCenter
            
            //font: UM.Theme.getFont("default")
            font.underline: true
            color: '#0000ff'
            text: 'Teton Simulation'
            onLinkActivated: Qt.openUrlExternally(link)

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally('https://tetonsim.com')
            }
        }
        
        Text {
            id: statusText
            
            Layout.alignment: Qt.AlignCenter
            
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            
            text: aboutText
        }
        
        Button {
            Layout.alignment: Qt.AlignCenter

            text: catalog.i18nc("@action:button", "Close")
            onClicked: aboutDialog.close()
        }
    }
}
