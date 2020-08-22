from flask import Blueprint, render_template,  url_for, request, g, flash
from werkzeug.utils import redirect
from ..forms import Profilemodi
from .auth_views import login_required
from pybo.models import User, Myprofile
from pybo import db
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('question._list')) # question_view의 list 함수로 이동




