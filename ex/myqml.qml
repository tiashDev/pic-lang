import QtQuick 2.12

Rectangle {
    id: colorbutton
    width: 200; height: 80;

    color: inputHandler.pressed ? "steelblue" : "lightsteelblue"

    TapHandler {
        id: inputHandler
    }
}