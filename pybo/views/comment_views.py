from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Comment,Answer
from pybo.views.auth_views import login_required
from pybo.models import Question1, Comment1, Answer1
bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/question/<int:x>/<int:question_id>', methods=('GET', 'POST'))
@login_required
def create_question(question_id, x):
    if x == 0:
        question_0 = Question
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:
        question_0 = Question1
        comment_0 = Comment1
        xx = 'question.detail1'
    form = CommentForm()
    question = question_0.query.get_or_404(question_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = comment_0(user=g.user, content=form.content.data, create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(
            url_for(xx, question_id=question_id), comment.id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/question/<int:x>/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id, x):
    if x == 0:
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:
        comment_0 = Comment1
        xx = 'question.detail1'
    comment = comment_0.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for(xx, question_id=comment.question.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(
                url_for(xx, question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

@bp.route('/delete/question/<int:x>/<int:comment_id>')
@login_required
def delete_question(comment_id,x):
    if x == 0:
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:
        comment_0 = Comment1
        xx = 'question.detail1'

    comment = comment_0.query.get_or_404(comment_id)
    question_id = comment.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for(xx, question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for(xx, question_id=question_id))


@bp.route('/create/answer/<int:x>/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id, x):
    if x == 0:
        answer_0 = Answer
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:
        answer_0 = Answer1
        comment_0 = Comment1
        xx = 'question.detail1'

    form = CommentForm()
    answer = answer_0.query.get_or_404(answer_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = comment_0(user=g.user, content=form.content.data, create_date=datetime.now(), answer=answer)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(
            url_for(xx, question_id=answer.question.id), comment.id))
    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/answer/<int:x>/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id, x):
    if x == 0:
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:

        comment_0 = Comment1
        xx = 'question.detail1'
    comment = comment_0.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for(xx, question_id=comment.answer.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(
                url_for(xx, question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/answer/<int:x>/<int:comment_id>')
@login_required
def delete_answer(comment_id, x):
    if x == 0:
        comment_0 = Comment
        xx = 'question.detail'
    elif x == 1:
        comment_0 = Comment1
        xx = 'question.detail1'
    comment = comment_0.query.get_or_404(comment_id)
    question_id = comment.answer.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for(xx, question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for(xx, question_id=question_id))
