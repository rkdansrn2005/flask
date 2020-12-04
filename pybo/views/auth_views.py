from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
# 보안 강화
from werkzeug.utils import redirect

from pybo import db

from pybo.forms import UserCreateForm, UserLoginForm

from ..forms import Profilemodi

from pybo.models import User, Myprofile
from datetime import datetime
bp = Blueprint('auth', __name__, url_prefix='/auth')

import functools

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.registerclear'))

            except:
                db.session.rollback()
                flash('가입 실패- 이메일을 확인해주세요')

            return redirect(url_for('main.registerclear'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            # 로그인 되었을때 session 변수에 User의 id값을 저장하면
            # 브라우저 요청이 발생할 경우 이 세션값으로 사용자가
            # 로그인한 사용자인지 아닌지를 판별할 수 있게 됨
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# @bp.before_app_request 어노테이션은 플라스크에서 제공하는
# 기능으로 이 어노테이션이 적용된 함수는 라우트 함수 실행전에
# 항상 먼저 실행된다. 따라서 load_logged_in_user 함수는
# 모든 라우트 함수 실행전에 반드시 먼저 실행될 것이다.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# 다른 함수에서 @login_required 라는 어노테이션을 지정하면 login_required라는 데코레이터 함수가 먼저 실행
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#
@bp.route('/profilemodify/<gg>', methods=(['GET', 'POST']))
@login_required
def profilemodify(gg):
    form = Profilemodi()
    if g.user:
        if request.method == 'POST' and form.validate_on_submit():
            user = Myprofile.query.filter_by(username=gg).first()

            user.email = form.email.data
            user.real_name = form.real_name.data
            user.age = form.age.data
            user.address = form.address.data
            user.hoby = form.hoby.data

            user.introduce = form.introduce.data
            user.cellphone = form.cellphone.data
            user.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            return render_template('auth/profile.html', form=form)
    else:
        flash("권한이 없습니다.")

    return redirect(url_for('question._list'))
