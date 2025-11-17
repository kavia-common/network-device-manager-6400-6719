from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_restful import Api as RestfulApi
from .routes.health import blp
from .resources import DevicesResource, DeviceResource, PingResource

# Initialize Flask app and APIs
app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable CORS for future frontend consumption
CORS(app, resources={r"/*": {"origins": "*"}})

# Swagger/OpenAPI docs config (served by flask-smorest)
app.config["API_TITLE"] = "Network Device Manager REST API"
app.config["API_VERSION"] = "1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Setup smorest for docs and register existing health blueprint
api = Api(app)
api.register_blueprint(blp)

# Setup Flask-RESTful for the required resources
rest_api = RestfulApi(app, prefix="")
rest_api.add_resource(DevicesResource, "/devices", endpoint="devices")
rest_api.add_resource(DeviceResource, "/devices/<string:name>", endpoint="device")
rest_api.add_resource(PingResource, "/ping/<string:name>", endpoint="ping")
