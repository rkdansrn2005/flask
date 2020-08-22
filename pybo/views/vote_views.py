from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from pybo.models import Question1, Answer1
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/question/<int:x>/<int:question_id>/')
@login_required
def question(question_id,x):
    if x == 0:
        question_0 = Question
        xx = 'question.detail'
    elif x == 1:
        question_0 = Question1
        xx = 'question.detail1'
    _question = question_0.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for(xx, question_id=question_id))

@bp.route('/answer/<int:x>/<int:answer_id>/')
@login_required
def answer(answer_id, x):
    if x == 0:
        answer_0 = Answer
        xx = 'question.detail'
    elif x == 1:
        answer_0 = Answer1
        xx = 'question.detail1'
    _answer = answer_0.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for(xx, question_id=_answer.question.id))