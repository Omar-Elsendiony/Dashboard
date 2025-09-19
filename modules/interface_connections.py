from flask import Blueprint, render_template

interface_connections_bp = Blueprint('interface_connections', __name__)

@interface_connections_bp.route('/', strict_slashes=False, methods=["GET", "POST"])
def interface_connections():
    return render_template('interface_connections.html')