import QtQuick 2.15
import QtQuick.Controls 2.15
import "main.js" as JSMain

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    x: screen.desktopAvailableWidth - width - 12
    y: screen.desktopAvailableHeight - height - 48
    title: "Clock"
    flags: Qt.FramelessWindowHint | Qt.Window
    property string currTime: "00:00:00"
    property var hms: {'hours': 0, 'minutes': 0, 'seconds': 0}
	Timer {
        interval: 500;
		running: true; 
		repeat: true;
        onTriggered: JSMain.onTimeout();
    }
		
		
    color: "transparent"


    Image {
        id: clockface
        sourceSize.width: parent.width
        fillMode: Image.PreserveAspectFit
        source: "./images/clockface.png"
		antialiasing: true

        Image {
            x: clockface.width/2 - width/2
            y: (clockface.height/2) - height/2
            scale: clockface.width/465
            source: "./images/hour.png"
			antialiasing: true
            transform: Rotation {
                    origin.x: 12.5; origin.y: 166;
                    angle: (hms.hours * 30) + (hms.minutes * 0.5)
            }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "./images/minute.png"
            scale: clockface.width/465
			antialiasing: true
            transform: Rotation {
                    origin.x: 5.5; origin.y: 201;
                    angle: hms.minutes * 6
                    Behavior on angle {
                        SpringAnimation { spring: 1; damping: 0.2; modulus: 360 }
                    }
                }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "./images/second.png"
            scale: clockface.width/465
			antialiasing: true
            transform: Rotation {
                    origin.x: 2; origin.y: 202;
                    angle: hms.seconds * 6
                    Behavior on angle {
                        SpringAnimation { spring: 3; damping: 0.2; modulus: 360 }
                    }
                }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "./images/cap.png"
			antialiasing: true
            scale: clockface.width/465
        }

    }
}