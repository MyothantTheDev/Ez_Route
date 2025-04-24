from src.ez_route.registry import RouteMap
from src.ez_route.route import Route
from src.ez_route.manager import RouteManager

class Router:

  def __init__(self):
    self.route_map = RouteMap()
    self.mangaer = RouteManager(self.route_map)
    self.history = []

  def install_route(self, route: Route):
    """
    Register a route in the router.
    """
    if not isinstance(route, Route):
      raise TypeError("Route should be an instance of Route.")
    
    if route.node.name in self.route_map.routeMapByName.keys():
      raise ValueError(f"Route with name {route.node.name} already exists.")
    
    if route.node.path in self.route_map.routeMapByPath.keys():
      raise ValueError(f"Route with path {route.node.path} already exists.")
    
    self.route_map.register_route(route)
    
    if len(route.children) > 0:
      for child in route.children:
        self.install_route(child)


  def go_by_name(self, name: str, params = {}) -> object:
    """
    Get a route by its name.
    """
    route = self.mangaer.get_route_by_name(name)
    return self.__build_screen(route, params)
  
  def go_by_path(self, path: str) -> Route:
    """
    Get a route by its path.
    """
    route, params = self.mangaer.get_route_by_path(path)
    return self.__build_screen(route, params)
  
  def __build_screen(self, route: Route, params = {}) -> Route:
    """
    Register the route in the history.
    """
    if not isinstance(route, Route):
      raise TypeError("Route should be an instance of Route.")
    
    if not isinstance(params, dict):
      raise TypeError("Params should be a dictionary.")
    
    screen = route.build_screen(**params)
    self.history.append(route)
    return screen
  
  def get_history(self) -> list[Route]:
    """
    Get the history of routes.
    """
    return self.history
  
  def clear_history(self):
    """
    Clear the history of routes.
    """
    self.history.clear()

  def go_back(self):
    """
    Go back to the previous route.
    """
    if len(self.history) > 1:
      self.history.pop()
      return self.history[-1]
    
    return None