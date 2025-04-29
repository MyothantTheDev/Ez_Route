import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from src.ez_route import Router, QtRoute, ServiceLocator

class AboutScreen(QWidget):
  def __init__(self,):
    super().__init__()
    self.router = ServiceLocator.get("router")
    self.setup_ui()

  def setup_ui(self):
    layout = QVBoxLayout()

    title = QLabel("About Screen")
    title.setStyleSheet("font-size: 24px;")

    about_button = QPushButton("Go to Home Page")
    about_button.clicked.connect(self.go_to_home)

    layout.addWidget(title)
    layout.addWidget(about_button)
    self.setLayout(layout)

  def go_to_home(self):
    self.router.go_by_path('/home')

class HomeScreen(QWidget):
  def __init__(self,):
    super().__init__()
    self.router = ServiceLocator.get("router")
    self.setup_ui()

  def setup_ui(self):
    layout = QVBoxLayout()

    title = QLabel("Home Screen")
    title.setStyleSheet("font-size: 24px;")

    about_button = QPushButton("Go to About Page")
    about_button.clicked.connect(self.go_to_about)

    layout.addWidget(title)
    layout.addWidget(about_button)
    self.setLayout(layout)

  def go_to_about(self):
    self.router.go_by_path('/about')



class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    root = QtRoute(path='/', screen=self)
    home = QtRoute(path='/home', screen=HomeScreen)
    about = QtRoute(path='/about', screen=AboutScreen)
    self.router = Router(self)
    self.router.install_route(root)
    self.router.install_route(home)
    self.router.install_route(about)
    ServiceLocator.provide("router", self.router)
    self.router.go_by_path('/home')

if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  sys.exit(app.exec())