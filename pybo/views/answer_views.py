from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g,flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from pybo.models import Question1, Answer1
# 자동 화면 이동 auth_views의  login_required 함수 실행
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


# @bp.route('/create/<int:question_id>', methods=('POST', ))
# def create(question_id):
#     question = Question.query.get_or_404(question_id)
#     content = request.form['content']
#     answer = Answer(question=question, content=content, create_date=datetime.now())
#     db.session.add(answer)
#     # answer = Answer(content=content, create_date=datetime.now())
#     # question.answer_set.append(answer)
#     db.session.commit()
#     return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/create/<int:x>/<int:question_id>', methods=('POST', ))
@login_required
def create(question_id, x):
    if x == 0:
        question_0 = Question
        answer_0 = Answer
        xx = 'question.detail'
        xxx= 'question/question_detail.html'
    elif x == 1:
        question_0 = Question1
        answer_0 = Answer1
        xx = 'question.detail1'
        xxx ='question/question_detail1.html'
    form = AnswerForm()
    question = question_0.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = answer_0(question=question, content=content, create_date=datetime.now(), user=g.user)

        db.session.add(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for(xx, question_id=question_id), answer.id))
    return render_template(xxx, question=question, form=form)

@bp.route('/modify/<int:x>/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id, x):
    if x == 0:
        answer_0= Answer
        xx = 'question.detail'
    elif x == 1:
        answer_0 = Answer1
        xx = 'question.detail1'
    answer = answer_0.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for(xx, question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for(xx, question_id=answer.question.id), answer.id))

    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:x>/<int:answer_id>')
@login_required
def delete(answer_id, x):
    if x == 0:
        answer_0= Answer
        xx = 'question.detail'
    elif x == 1:
        answer_0 = Answer1
        xx = 'question.detail1'
    answer = answer_0.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for(xx, question_id=question_id))