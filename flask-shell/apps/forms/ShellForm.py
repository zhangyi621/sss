from wtforms import Form, validators, ValidationError
from wtforms import StringField, PasswordField

from apps.models.login_model import ShellModel


# 商家注册form验证
class ShellRegisterForm(Form):
    username = StringField(label="用户名", validators=[validators.DataRequired(message="必填项"),
                                                    validators.Length(min=6, message="用户名不能少于6位"),
                                                    validators.Length(max=16, message="用户名不能多于16位")
                                                    ],
                           render_kw={"class": "form-control", "placeholder": "用户名"}
                           )
    password = PasswordField(label="密码", validators=[validators.DataRequired(message="必填项"),
                                                     validators.Length(min=6, message="密码长度不能小于6位")
                                                     ],
                             render_kw={"class": "form-control", "placeholder": "密码"}
                             )
    pwd2 = PasswordField(label="确认密码", validators=[validators.EqualTo("password", message="两次密码不一致")],
                         render_kw={"class": "form-control", "placeholder": "确认密码"}
                         )

    def validate_username(self, form):
        username = form.data
        data = ShellModel.query.filter_by(username=username).all()
        if data:
            raise ValidationError("用户已存在")


# 商家登录form
class ShellLoginForm(Form):
    username = StringField(label="用户名", validators=[validators.DataRequired(message="必填项")],
                           render_kw={"class": "form-control", "placeholder": "用户名"}
                           )
    password = PasswordField(label="密码", validators=[validators.DataRequired(message="必填项")],
                             render_kw={"class": "form-control", "placeholder": "用户名"}
                             )
