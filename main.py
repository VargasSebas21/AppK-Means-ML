from flask_instance import FlaskInstance
from kmeans import Kmeans

class Main:
  flask_instance = FlaskInstance().__get_instance__
  app = flask_instance.get_app
  controller = Kmeans()

  def __init__(self):
    self.flask_instance.set_prefix('/api/')
    self.flask_instance.add_endpoint('kmeans', 'kmeans', self.controller.kmeans, ['get'])
    self.flask_instance.add_endpoint('predict', 'predict', self.controller.predict, ['get'])
    self.flask_instance.run()

if __name__ == "__main__":
  Main()