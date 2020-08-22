from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# wtforms를 이용하여 쉽게 form을 만들 수 있다.


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    # "제목"은 폼 라벨(Label)
    # validators는 검증을 위해 사용되는 도구로 필수 항목인지를
    # 체크하는 DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length 등이 있다.
    # validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는
    # DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length 등이 있다.
    # validators = [DataRequired(), Email()] 처럼 사용한다.
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(), Email("이메일 양식을 지켜주세요")])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired("아이디 오류"), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호오류')])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])

class Profilemodi(FlaskForm):
    email = EmailField('이메일', [DataRequired(), Email("이메일 양식을 지켜주세요")])
    real_name = StringField('실명', validators=[DataRequired(), Length(min=3, max=25)])
    age = IntegerField('나이', validators=[DataRequired()])
    address = StringField('주소', validators=[DataRequired(), Length(min=3, max=25)])
    hoby = TextAreaField('취미', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    introduce = TextAreaField('자기소개', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    cellphone = StringField('휴대폰 번호', validators=[DataRequired(), Length(min=3, max=25)])
