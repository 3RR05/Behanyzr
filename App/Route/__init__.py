from flask import Blueprint as bp

# For Main web interface
m_bp= bp('main', __name__)

# For API
a_bp= bp('api',__name__)

from App.Route import web_route, api_route