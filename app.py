import os
import sys

# Add the current directory to sys.path to ensure backend can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("🚀 PhishGuard Premium Server ready at http://localhost:5000")
    # Using socketio.run for real-time dashboard support
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
