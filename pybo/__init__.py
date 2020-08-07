from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

from flaskext.markdown import Markdown

# db 관련 문제 해결방안 2 키의 종류 지정
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
# SQLite 데이터베이스에서 사용하는 인덱스등의 제약조건의 이름규칙을 MetaData 클래스를
# 사용하여 정의해 주어야 한다. 이렇게 이름을 정의하지 않으면 SQLite 데이터베이스는 다음과 같은 오류를 발생시킨다.
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    # config에 작성한 환경 변수를 가지고 온다.
    app.config.from_object(config)

    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # db를 가동
    db.init_app(app)
    # 환경에 맞는 config를 찾아서 해당 환경에 적혀져 있는 DB주소로 마이그레이션이 진행된다.


    # db 관련 문제 해결방안 2
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
        #  render_as_batch=False 면 
        # ERROR [root] Error: No support for ALTER of constraints in SQLite 
        # dialectPlease refer to the batch mode feature which allows for SQLite 
        # migrations using a copy-and-move strategy. 오류 발생
    else:
        migrate.init_app(app, db)
        # SQLite 데이터베이스에서 사용하는 인덱스등의 제약조건의 이름규칙을 MetaData 클래스를
        # 사용하여 정의해 주어야 한다. 이렇게 이름을 정의하지 않으면 SQLite 데이터베이스는
        # ValueError: Constraint must have a name 오류를 발생시킨다.
    # 하고 flask db migrate flask db upgrade를 통해 db를 수정한다.

    # models을 가져와서
    from . import models
    # 우리가 작성한 모델인 models.py 파일을 참조할

    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views

    app.register_blueprint(main_views.bp) # mainveiw의 bp실행
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    from .filter import format_datetime
    # 날짜 함수 활용하여 보기 편하게 변경 date형식을 바꿈 앞으로 | + datetime 을 뒤에 붙이면 다 이 형식이 된다.
    app.jinja_env.filters['datetime'] = format_datetime


    return app
