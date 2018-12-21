from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


# 实例化空db对象
db = SQLAlchemy()


# 基础模型类
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    is_delete = db.Column(db.Integer, default=0)

    def set_attrs(self, dic):
        for k, v in dic.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)


# 加载模型类
from apps.models import login_model
from apps.models import shop_model
from apps.models import dishes_category_model
from apps.models import dishes_info_model
from apps.models import todo_user
from apps.models import order_model