from pybo import db # pybo/__init__.py 에서 생성한 SQLAlchemy의 객체


# _____로그인

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Myprofile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), db.ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    profile = db.relationship('User', backref=db.backref('profile_set'))

    real_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    hoby = db.Column(db.String(200), nullable=True)
    introduce = db.Column(db.String(200), nullable=True)
    cellphone = db.Column(db.String(50), nullable=True)
    modify_date = db.Column(db.DateTime(), nullable=True)


# 제 1 게시판_______________________________

# 추천(좋아요) 만드는 방식
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)



class Question(db.Model): # 하나의 테이블 만들어짐 pybo라는 db에
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),  nullable=False)
    # 왜 오류가 발생했냐면 이미 기존 id없는 계정이 존재 그래서 defaut 값 전달 후
    # null=false를 사용하려면 nullable = True 하고 flask db migrate 명령과 flask db upgrade 명령
    # null=false로 다시 바꿔준후 flask db migrate 명령과 flask db upgrade
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    look = db.Column(db.Integer, nullable =False, server_default='1')
    # 계정과 질문이 모두 프라이머리키이므로 ManyToMany  + 속성의 이름 지정 question_voter_set
 #  어떤 계정이 a_user 라는 객체로 참조되었다면 a_user.question_voter_set 으로 해당 계정이 추천한 질문 리스트를 구할수 있게 된다
   # 여기서는 User.question_voter_set 으로 참조 가능


answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)


class Answer(db.Model): # 하나의 테이블을 생성
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # question_id는 클래스 question의 id와 연결되어 있음며 참조됨
    # backref 속성은 answer.question.subject 와는 반대로 질문에서 답변모델을 참조하기 위해서
    # 사용되는 속성이다. 하나의 질문에는 여러개의 답변이 작성될 수 있는데 어떤 질문에 해당되
    # 는 객체가 a_question 이라면 이 질문에 작성된 답변들을 참조하기 위해서
    # a_question.answer_set 과 같이 사용할 수 있다.
    # 즉 answer_set을 통해 question.id로부터 관련된 것들을 Answer table로 부터 가져올 수 있다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))




class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

# #___________________________________________________________________________

# 제 2 게시판_______________________________

# 추천(좋아요) 만드는 방식

question_voter1 = db.Table(
    'question_voter1',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question1.id', ondelete='CASCADE'), primary_key=True)
)




class Question1(db.Model):
    # 하나의 테이블 만들어짐 pybo라는 db에
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),  nullable=False)
    # 왜 오류가 발생했냐면 이미 기존 id없는 계정이 존재 그래서 defaut 값 전달 후
    # null=false를 사용하려면 nullable = True 하고 flask db migrate 명령과 flask db upgrade 명령
    # null=false로 다시 바꿔준후 flask db migrate 명령과 flask db upgrade
    user = db.relationship('User', backref=db.backref('question_set1'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter1, backref=db.backref('question_voter_set1'))
    look = db.Column(db.Integer, nullable =False, server_default='1')
    # 계정과 질문이 모두 프라이머리키이므로 ManyToMany  + 속성의 이름 지정 question_voter_set
    #  어떤 계정이 a_user 라는 객체로 참조되었다면 a_user.question_voter_set 으로 해당 계정이 추천한 질문 리스트를 구할수 있게 된다
    # 여기서는 User.question_voter_set 으로 참조 가능


answer_voter1 = db.Table(
    'answer_voter1',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer1.id', ondelete='CASCADE'), primary_key=True)
)


class Answer1(db.Model): # 하나의 테이블을 생성
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question1.id', ondelete='CASCADE'))
    question = db.relationship('Question1', backref=db.backref('answer_set1'))
    # question_id는 클래스 question의 id와 연결되어 있음며 참조됨
    # backref 속성은 answer.question.subject 와는 반대로 질문에서 답변모델을 참조하기 위해서
    # 사용되는 속성이다. 하나의 질문에는 여러개의 답변이 작성될 수 있는데 어떤 질문에 해당되
    # 는 객체가 a_question 이라면 이 질문에 작성된 답변들을 참조하기 위해서
    # a_question.answer_set 과 같이 사용할 수 있다.
    # 즉 answer_set을 통해 question.id로부터 관련된 것들을 Answer table로 부터 가져올 수 있다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set1'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter1, backref=db.backref('answer_voter_set1'))




class Comment1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set1'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question1.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question1', backref=db.backref('comment_set1'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer1.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer1', backref=db.backref('comment_set1'))

#___________________________________________________________________________