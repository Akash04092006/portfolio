"""
WSGI Application Entrypoint for Vercel Serverless Functions.
Exports the Flask 'app' instance for runtime execution.
"""
import os
import sys

# Ensure project root is in Python module search path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app

# For direct local invocation or container runtimes
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
