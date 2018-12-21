from flask_login import UserMixin

from apps import login_manager
from apps.models import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class ShellModel(BaseModel, UserMixin):
    username = db.Column(db.String(32))
    _password = db.Column('password', db.String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, data):
        self._password = generate_password_hash(data)

    def check_password(self, data):
        return check_password_hash(self.password, data)


# 将数据模型类注册到login插件中,给一个userid,将我们自己的数据模型对象给login插件
@login_manager.user_loader
def load_user(userid: str):
    return ShellModel.query.filter_by(id=int(userid)).first()
