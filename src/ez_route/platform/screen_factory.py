from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget
from tkinter.ttk import Frame

class BaseScreenFactory(ABC):

  @abstractmethod
  def create(self, screen: QWidget | Frame, **params):
    pass

class QtScreenFactory(BaseScreenFactory):

  instances: dict[str, QWidget] = {}

  def create(self, screen: QWidget, **params):
    if screen not in self.instances:
      self.instances[screen] = screen()
    if hasattr(self.instances[screen], "with_param") and params:
      return self.instances[screen].with_param(**params)
    return self.instances[screen]
  

class TkScreenFactory(BaseScreenFactory):

  main_frame: Frame = None
  instances: dict[str, Frame] = {}

  def create(self, screen: Frame, **params) -> Frame:
    if screen not in self.instances:
      self.instances[screen] = screen(self.main_frame)
    if hasattr(self.instances[screen], "with_param") and params:
      return self.instances[screen].with_param(**params)
    return self.instances[screen]
  
  def set_mainFrame(self, main_frame: Frame):
    self.main_frame = main_frame