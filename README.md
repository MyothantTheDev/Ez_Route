

# Ez_Route 🧭
**Lightweight routing system for Python GUI applications (Tkinter & PyQt6)**

**Ez_Route** is a minimal routing library for GUI frameworks like **Tkinter** and **PyQt6**, offering **path-based** and **named route navigation**, **nested routing**, and **parameter passing**. Inspired by SPA routing frameworks, it brings a structured way to manage screen transitions in Python desktop apps.

---

## ✨ Features

- ✅ Simple route declaration and registration
- ✅ Named routes with path matching
- ✅ Dynamic segments (e.g., `/user/:id`)
- ✅ Nested routes and history support
- ✅ GUI-agnostic: works with both **Tkinter** and **PyQt6**
- ✅ Customizable and extensible architecture

---

## Get Started

### Install
```bash
pip install ez-route
```
---

### Example: 
#### PyQt Usage

```python
import  sys
from  PySide6.QtWidgets  import  QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from  ez_route  import  Router, QtRoute, ServiceLocator

  

class  AboutScreen(QWidget):

	def  __init__(self,):
		super().__init__()
		self.router  =  ServiceLocator.get("router")
		self.setup_ui()

	def  setup_ui(self):
		layout  =  QVBoxLayout()
		title  =  QLabel("About Screen")
		title.setStyleSheet("font-size: 24px;")
		about_button  =  QPushButton("Go to Home Page")
		about_button.clicked.connect(self.go_to_home)
		layout.addWidget(title)
		layout.addWidget(about_button)
		self.setLayout(layout)

	def  go_to_home(self):
		self.router.go_by_path('/home')

  

class  HomeScreen(QWidget):

	def  __init__(self,):
		super().__init__()
		self.router  =  ServiceLocator.get("router")
		self.setup_ui()

  

	def  setup_ui(self):
		layout  =  QVBoxLayout()
		title  =  QLabel("Home Screen")
		title.setStyleSheet("font-size: 24px;")
		about_button  =  QPushButton("Go to About Page")
		about_button.clicked.connect(self.go_to_about)
		layout.addWidget(title)
		layout.addWidget(about_button)
		self.setLayout(layout)

	def  go_to_about(self):
		self.router.go_by_path('/about')

class  MainWindow(QMainWindow):

	def  __init__(self):
		super().__init__()
		root  =  QtRoute(path='/', screen=self)
		home  =  QtRoute(path='/home', screen=HomeScreen)
		about  =  QtRoute(path='/about', screen=AboutScreen)
		self.router  =  Router(self)
		self.router.install_route(root)
		self.router.install_route(home)
		self.router.install_route(about)
		ServiceLocator.provide("router", self.router)
		self.router.go_by_path('/home')

  

if  __name__  ==  "__main__":
	app  =  QApplication([])
	window  =  MainWindow()
	window.show()
	sys.exit(app.exec())
```

#### Tkinter Usage
```python
import  tkinter  as  tk
from  ez_route  import  Router, TkRoute, ServiceLocator

class  ProfileDetailPage(tk.Frame):
	def  __init__(self, main_frame):
		super().__init__(main_frame)
		self.router  =  ServiceLocator.get("router")
		self.label  =  tk.Label(self, text="Profile Page", font=("Arial", 16))
		self.label.pack(pady=10)
		btn  =  tk.Button(self, text="Go to Home Page",
		command=  lambda: self.router.go_by_path("/home"))
		btn.pack(pady=10)
		
	def  with_param(self, **params):
		self.label  =  tk.Label(self, text=f"Profile Page - Params {params.get('id')}", font=("Arial", 16))
		self.label.pack(pady=10)

class  ProfilePage(tk.Frame):
	def  __init__(self, main_frame):
		super().__init__(main_frame)
		self.router  =  ServiceLocator.get("router")
		self.label  =  tk.Label(self, text="Profile Page", font=("Arial", 16))
		self.label.pack(pady=10)
		btn  =  tk.Button(self, text="Go to Detial Page with Params",command=  lambda: self.router.go_by_path("/profile/2893"))
		btn.pack(pady=10)

class  HomePage(tk.Frame):
	def  __init__(self, main_frame):
		super().__init__(main_frame)
		self.router  =  ServiceLocator.get("router")
		self.label  =  tk.Label(self, text="Home Page", font=("Arial", 16))
		self.label.pack(pady=10)
		btn  =  tk.Button(self, text="Go to Profile Page",command=  lambda: self.router.go_by_path("/profile"))
		btn.pack(pady=10)

class  App(tk.Tk):

	def  __init__(self):
		super().__init__()
		self.title("Tkinter Nested Pages with Parameters")
		self.geometry("500x300")
		container  =  tk.Frame(self)
		container.pack(fill="both", expand=True)
		self.router  =  Router(container)
		ServiceLocator.provide("router", self.router)
		home  =  TkRoute(path='/home', screen=HomePage)
		profile  =  TkRoute(path='/profile', screen=ProfilePage)
		profile_detail  =  TkRoute(path='/:id', screen=ProfileDetailPage, route_name="profile-detail")
		profile.add_child_route(profile_detail)
		self.router.install_route(home)
		self.router.install_route(profile)
		self.router.go_by_path("/home")

if  __name__  ==  "__main__":
	app  =  App()
	app.mainloop()
```


## 🧩 Core Components

###  `Router`

Main entry point to register and navigate routes.

```Router(main_frame: tk.Frame | QWidget)```

#### Methods:

-   `install_route(route: Route)`  
    Register a new route and its children.
    
-   `go_by_name(name: str, params: dict = {})`  
    Navigate to a route by its name and pass optional parameters.
    
-   `go_by_path(path: str)`  
    Navigate to a route by its path.
---
### 🧭 `Route` (Base Class)

Base class to define a route node.

`Route(path: str, screen: Callable, route_name: Optional[str] = None)` 

#### Attributes:

-   `path: str`: Route path (can be dynamic like `/:id`)
    
-   `screen: Callable`: A factory or class used to render the screen
    
-   `route_name: Optional[str]`: Name of the route for name-based navigation
    
-   `children: List[Route]`: Nested child routes   

#### Methods:

-   `add_child_route(child: Route)` – Nest a child route under this route.
-   `add_children_routes(children: List[Route])` – Nest a list of children routes under this route.
-  `display(main_frame: tk.Frame | QWidget, **params)` – This method is the `abstract method` 

---
    
### 🧭 `TkRoute`

A `Route` implementation for tkinter apps using `tk.Frame`.

`TkRoute(path: str, screen: type[tk.Frame], route_name: str = None)` 

#### Attributes:

-   `path`: URL-style route path (`"/home"`, `"/settings"`, etc.)
    
-   `screen`: The `tk.Frame`-based class to be shown
    
-   `route_name`: Optional unique name for named navigation
    

#### Methods:

-   `display(main_frame: tk.Frame, **params)`  
    Shows the associated screen inside `main_frame`. Calls `tkraise()` and passes `params` if supported.
---
### 🧭 `QtRoute`

A `Route` implementation for tkinter apps using `QWidget`.
`QtRoute(path: str, screen: type[QWidget], route_name: str = None)` 

#### Attributes:

-   `path`: URL-style route path (`"/home"`, `"/settings"`, etc.)
    
-   `screen`: The `QWidget`-based class to be shown
    
-   `route_name`: Optional unique name for named navigation
    

#### Methods:

-   `display(main_frame: QMainWindow, **params)`  
    Shows the associated screen inside `main_frame`. Calls `setCentralWidget` and passes `params` if supported.
---
## 🧰 Service Locator

### `ServiceLocator`

A global object registry for dependency injection (e.g., Router access from pages).

#### Methods:

`provide(name: str, instance: Any)`
`get(name: str) -> Any`

Used for accessing shared services like the router across screens.

---

