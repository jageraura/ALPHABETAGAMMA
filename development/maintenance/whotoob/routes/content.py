from flask import Blueprint, render_template
from flask_login import login_required, current_user

content_bp = Blueprint('content', __name__)

@content_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@content_bp.route('/premium')
@login_required
def premium_content():
    if current_user.is_premium:
        return render_template('premium.html')
    return "Upgrade to access premium content!", 403
