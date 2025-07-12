from flask import Blueprint
from auth import auth_bp

# Re-export the auth blueprint
auth_blueprint = auth_bp

