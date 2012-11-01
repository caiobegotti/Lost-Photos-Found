import QtQuick 1.0
import Qt.labs.folderlistmodel 1.0

Rectangle {
    width: 800
    height: 600

    GridView {
        anchors.fill: parent
        cellWidth: 128
        cellHeight: 128

        model: FolderListModel {
            id: folderModel
            nameFilters: ["*.png"]
        }

        delegate: Image {
            source: fileName
            width: 128
            height: 128
        }
    }

    Timer {
        interval: 500; running: true; repeat: true
        onTriggered: folderModel.submit
    }
}
