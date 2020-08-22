
from flask import Blueprint, render_template, request, url_for, g, flash

from datetime import datetime
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User, question_voter

from ..models import Question1, Answer1,  question_voter1
# from ..models import Question1, Answer1, question_voter1

from ..forms import QuestionForm, AnswerForm
# 자동 화면 이동 auth_views의  login_required 함수 실행
from pybo.views.auth_views import login_required

# sql 기능과 null 값을 마지막으로 이동
from sqlalchemy import func
from sqlalchemy import nullslast

bp = Blueprint('question', __name__, url_prefix='/question')
# main' 이라는 이름은 나중에 함수명으로 URL을 찾아내는 url_for 함수에서 사용
# URL 프리픽스(url_prefix)는 main_views.py 파일에 있는 함수들의 URL 앞에 항상 붙게 되는
# 프리픽스 URL을 의미한다. 만약 위에서 url_prefix='/' 대신 url_prefix='/main' 이라고 선언했다면
# hello_pybo 함수를 호출하기 위해서는 http://localhost:5000/ 대신 http://localhost:5000/question/ 이라고 호출해야 한다.

@bp.route('/list/')
def _list():
    a = 0
    if a == 0:
        question_0 = Question
        answer_0 = Answer
        a = 0
    else:
        a = 1
        pass

    page = request.args.get('page', type=int, default=1)
    # GET방식으로 요청한 URL에서 page의 값을 가져옴
    # ex  http://localhost:5000/question/list/?page=1

    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = question_0.query \
            .outerjoin(sub_query, question_0.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), question_0.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(answer_0.question_id, func.count('*').label('num_answer')) \
            .group_by(answer_0.question_id).subquery()
        question_list = question_0.query \
            .outerjoin(sub_query, question_0.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), question_0.create_date.desc())
    else:  # recent
        question_list = question_0.query.order_by(question_0.create_date.desc())


    #  검색
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(answer_0.question_id, answer_0.content, User.username) \
            .join(User, answer_0.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == question_0.id) \
            .filter(question_0.subject.ilike(search) |  # 질문제목
                    question_0.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    question_list = question_list.paginate(page, per_page=10)
    # 페이지네이션
    #  코드는 조회된 데이터에 페이징을 적용해 준다.
    # page는 현재 조회할 페이지번호를 의미하고 per_page=10 속성은 한 페이지에 보여줄 게시물의 갯수를 10건으로 하겠다는 의미이다.
    return render_template('question/question_list.html', question_list=question_list, page=page,
                           kw=kw, x=a)



@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    x=0
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    question.look += 1
    db.session.commit()
    return render_template('question/question_detail.html', question=question, form=form, x=x)

@bp.route('/create/<int:x>', methods=('GET', 'POST'))
@login_required
def create(x):
    form = QuestionForm()
    if x == 0:
        question_0 = Question
        xx = 'question._list'
    elif x == 1:
        question_0 = Question1
        xx = 'question._list1'

    if request.method == 'POST' and form.validate_on_submit():
        # POST로 전송된 폼 데이터의 정합성을 체크
        question = question_0(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for(xx))

    return render_template('question/question_form.html', form=form,x=x)

@bp.route('/modify/<int:x>/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id, x):
    # question_id는 question_list에서 클릭하면 url_for을 통하여 question.id를 받게 된다.
    if x == 0:
        question_0 = Question
        xx = 'question.detail'
    elif x == 1:
        question_0 = Question1
        xx = 'question.detail1'

    question = question_0.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for(xx, question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            # 수정이 발생함
            # form.populate_obj(question) 를 사용했는데 이것은
            # form으로 전달받은 데이터를 question 객체에 적용하는 역할
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for(xx, question_id=question_id))
    else:
        form = QuestionForm(obj=question)
        # QuestionForm(obj=question) 처럼 조회된 객체를 전달하여 폼을 생성
    return render_template('question/question_form.html', form=form, x=x)

@bp.route('/delete/<int:x>/<int:question_id>')
@login_required
def delete(question_id, x):
    if x == 0:
        question_0 = Question
        xx = 'question.detail'
        xxx = 'question._list'
    elif x == 1:
        question_0 = Question1
        xx = 'question.detail1'
        xxx = 'question._list1'
    question = question_0.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for(xx, question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for(xxx))

#############
@bp.route('/list1/')
def _list1():
    a = 1
    if a == 1:
        question_0 = Question1
        answer_0 = Answer1
        a = 1
    else:
        a = 1
        pass

    page = request.args.get('page', type=int, default=1)
    # GET방식으로 요청한 URL에서 page의 값을 가져옴
    # ex  http://localhost:5000/question/list/?page=1

    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')


    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter1.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter1.c.question_id).subquery()
        question_list = question_0.query \
            .outerjoin(sub_query, question_0.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), question_0.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(answer_0.question_id, func.count('*').label('num_answer')) \
            .group_by(answer_0.question_id).subquery()
        question_list = question_0.query \
            .outerjoin(sub_query, question_0.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), question_0.create_date.desc())
    else:  # recent
        question_list = question_0.query.order_by(question_0.create_date.desc())


    #  검색
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(answer_0.question_id, answer_0.content, User.username) \
            .join(User, answer_0.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == question_0.id) \
            .filter(question_0.subject.ilike(search) |  # 질문제목
                    question_0.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    question_list = question_list.paginate(page, per_page=10)
    # 페이지네이션
    #  코드는 조회된 데이터에 페이징을 적용해 준다.
    # page는 현재 조회할 페이지번호를 의미하고 per_page=10 속성은 한 페이지에 보여줄 게시물의 갯수를 10건으로 하겠다는 의미이다.
    return render_template('question/question_list1.html', question_list=question_list, page=page,
                           kw=kw, x=a)



@bp.route('/detail1/<int:question_id>/')
def detail1(question_id):
    x=1
    question_0 = Question1
    form = AnswerForm()
    question = question_0.query.get_or_404(question_id)
    question.look += 1
    db.session.commit()
    return render_template('question/question_detail1.html', question=question, form=form,x=x)
