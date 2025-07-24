# blueprints/settings.py

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from database.settings_db import get_analyze_mode, set_analyze_mode, get_user_settings, set_user_settings
from utils.session import check_session_validity
from utils.logging import get_logger

logger = get_logger(__name__)

settings_bp = Blueprint('settings_bp', __name__, url_prefix='/settings')

@settings_bp.route('/analyze-mode')
@check_session_validity
def get_mode():
    """Get current analyze mode setting"""
    try:
        return jsonify({'analyze_mode': get_analyze_mode()})
    except Exception as e:
        logger.error(f"Error getting analyze mode: {str(e)}")
        return jsonify({'error': 'Failed to get analyze mode'}), 500

@settings_bp.route('/analyze-mode/<int:mode>', methods=['POST'])
@check_session_validity
def set_mode(mode):
    """Set analyze mode setting"""
    try:
        set_analyze_mode(bool(mode))
        mode_name = 'Analyze' if mode else 'Live'
        return jsonify({
            'success': True, 
            'analyze_mode': bool(mode),
            'message': f'Switched to {mode_name} Mode'
        })
    except Exception as e:
        logger.error(f"Error setting analyze mode: {str(e)}")
        return jsonify({'error': 'Failed to set analyze mode'}), 500

@settings_bp.route('/', methods=['GET'])
@check_session_validity
def settings_page():
    """Render the settings page with user settings"""
    settings = get_user_settings()
    return render_template('settings.html', settings=settings)

@settings_bp.route('/update', methods=['POST'])
@check_session_validity
def update_settings():
    """Update user settings"""
    risk_appetite = request.form.get('risk_appetite')
    zerodha_api_key = request.form.get('zerodha_api_key')
    zerodha_api_secret = request.form.get('zerodha_api_secret')
    goal_short = request.form.get('goal_short')
    goal_medium = request.form.get('goal_medium')
    goal_long = request.form.get('goal_long')
    
    try:
        set_user_settings(risk_appetite, zerodha_api_key, zerodha_api_secret, goal_short, goal_medium, goal_long)
        flash('Settings updated successfully!', 'success')
    except Exception as e:
        logger.error(f"Error updating settings: {str(e)}")
        flash('Failed to update settings', 'danger')
    
    return redirect(url_for('settings_bp.settings_page'))
