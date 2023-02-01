import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from map import Ui_MainWindow

SCREEN_SIZE = [600, 450]


class StaticMap(QMainWindow, Ui_MainWindow):
    api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()
        self.setupUi(self)

    def getImage(self):
        self.current_ll = (37.530887, 55.703118)
        self.current_spn = (0.002, 0.002)
        self.type = 'map'
        params = {
            "ll": ",".join(map(str, self.current_ll)),
            "spn": ",".join(map(str, self.current_ll)),
            "l": self.type
        }
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        uic.loadUI('map.ui', self)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.changeMapScale('-')
        else:
            self.changeMapScale('+')
        self.get_Image()

    def changeMapScale(self, eventScaleType: str):
        current_change = 1
        if eventScaleType == '-':
            current_change = current_change
        new_spn = (self.current_spn[0] + current_change, self.current_spn[1] + current_change)
        if 0 <= new_spn[0] <= 90 and 0 <= new_spn[1] <= 90:
            self.current_spn = new_spn


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StaticMap()
    ex.show()
    sys.exit(app.exec())