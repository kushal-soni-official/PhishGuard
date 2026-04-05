from flask import Flask
from flask_cors import CORS
from phishguard.backend.config import Config
from phishguard.backend.extensions import socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    socketio.init_app(app)
    
    # Register blueprints
    from phishguard.backend.routes.api import api_bp
    from phishguard.backend.routes.web import web_bp
    
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting PhishGuard server on port 5000...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
