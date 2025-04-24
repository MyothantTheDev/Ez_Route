from src.ez_route.base import BaseNode, Expression, Literal, Variable
    
class RouteNode(BaseNode):
  def __init__(self, path, screen, name):
    super().__init__(path, screen, name)
    self.path = path
    self.screen = screen
    self.name = name
    self.pattern: list[Expression] = None

  def __repr__(self):
    return self.__class__.__name__

class Route:
  def __init__(self, path: str, screen: object, route_name: str = None):
    
    if not path.startswith("/"):
      raise Exception("Path should start with '/'")
    
    if route_name is None:
      route_name = self.__split_path(path)[0]
      if route_name.startswith(":"):
        raise Exception("Route that use parameter need speciific route name.")
    
    self.node = RouteNode(path, screen, route_name)
    self.children = []
    self.patter_process()

  def patter_process(self):
    """
    Process the path to create a pattern for matching using Interpreter Pattern.
    """
    self.node.pattern = []
    for segment in self.__split_path(self.node.path):
      if segment.startswith(":"):
        self.node.pattern.append(Variable(segment[1:]))
      else:
        self.node.pattern.append(Literal(segment))
  
  def add_child_route(self, route: 'Route'):
    """
    Add a child route to the current route.
    """
    if isinstance(route, Route):
      self.__process_child_path(route)
    else:
      raise TypeError("Route should be an instance of Route.")

  def add_children_routes(self, routes: list['Route'] | tuple['Route']):
    """
    Add multiple child routes to the current route.
    """
    if isinstance(routes, list) or isinstance(routes, tuple):
      for route in routes:
        self.add_child_route(route)

  def __process_child_path(self, route: 'Route'):
    route.node.path = '/'.join([*self.__split_path(self.node.path), *self.__split_path(route.node.path)])
    route.node.path = '/' + route.node.path
    route.patter_process()
    self.children.append(route)

  def __split_path(self, path: str):
    """
    Split the path into segments.
    """
    return path.strip("/").split("/")
  
  def build_screen(self, **params):
    """
    Build the widget using the screen and parameters.
    """
    screen = self.node.screen
    return screen(**params)