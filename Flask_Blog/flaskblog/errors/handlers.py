from flask import Blueprint, render_template
# this file is used to handle the errors got by inputing pages that are not in the app; errors like 404. Or other errors that has the default flask error handler outputing, but we are now using our own customized error page, rather than the default error page from flask engine

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

