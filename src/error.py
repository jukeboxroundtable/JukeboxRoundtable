from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.errorhandler(404)
def page_not_found(e):
    """Show the 404 page."""
    return render_template('404.html'), 404
