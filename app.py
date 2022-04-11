import os
from app import app

# Register Blueprints
from app.root.views import bp_root
from app.bungalows.views import bp_bungalows
from app.visitor.views import bp_visitor

app.register_blueprint(bp_root)
app.register_blueprint(bp_bungalows)
app.register_blueprint(bp_visitor)

if __name__ == "__main__":
    app.run(debug=True)