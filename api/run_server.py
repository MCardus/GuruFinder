"""Server execution"""

from api import create_app
from api.services import route

# Creating app
app = create_app(__name__)

# Attaching services to the app
app.register_blueprint(route)

# Running app
app.run(host="0.0.0.0", port=8837, threaded=True)
