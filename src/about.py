from flask import Blueprint, render_template

about = Blueprint('about', __name__)


@about.route('/about')
def about():
    """Show the about page."""
    return render_template('about.html')
