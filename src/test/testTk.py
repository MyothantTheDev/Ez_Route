import tkinter as tk
from src.ez_route import Router, TkRoute, ServiceLocator

class ProfileDetailPage(tk.Frame):
  def __init__(self, main_frame):
    super().__init__(main_frame)
    self.router = ServiceLocator.get("router")

    self.label = tk.Label(self, text="Profile Page", font=("Arial", 16))
    self.label.pack(pady=10)

    btn = tk.Button(self, text="Go to Home Page",
                    command= lambda: self.router.go_by_path("/home"))
    btn.pack(pady=10)

  def with_param(self, **params):
    self.label = tk.Label(self, text=f"Profile Page - Params {params.get('id')}", font=("Arial", 16))
    self.label.pack(pady=10)

class ProfilePage(tk.Frame):
  def __init__(self, main_frame):
    super().__init__(main_frame)
    self.router = ServiceLocator.get("router")

    self.label = tk.Label(self, text="Profile Page", font=("Arial", 16))
    self.label.pack(pady=10)

    btn = tk.Button(self, text="Go to Detial Page with Params",
                    command= lambda: self.router.go_by_path("/profile/2893"))
    btn.pack(pady=10)

class HomePage(tk.Frame):
  def __init__(self, main_frame):
    super().__init__(main_frame)
    self.router = ServiceLocator.get("router")

    self.label = tk.Label(self, text="Home Page", font=("Arial", 16))
    self.label.pack(pady=10)

    btn = tk.Button(self, text="Go to Profile Page",
                    command= lambda: self.router.go_by_path("/profile"))
    btn.pack(pady=10)

class App(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Tkinter Nested Pages with Parameters")
    self.geometry("500x300")

    container = tk.Frame(self)
    container.pack(fill="both", expand=True)

    self.router = Router(container)
    ServiceLocator.provide("router", self.router)

    home = TkRoute(path='/home', screen=HomePage)
    profile = TkRoute(path='/profile', screen=ProfilePage)
    profile_detail = TkRoute(path='/:id', screen=ProfileDetailPage, route_name="profile-detail")
    profile.add_child_route(profile_detail)

    self.router.install_route(home)
    self.router.install_route(profile)

    self.router.go_by_path("/home")

if __name__ == "__main__":
  app = App()
  app.mainloop()