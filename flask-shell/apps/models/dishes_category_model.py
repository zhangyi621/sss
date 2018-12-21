from apps.models import db, BaseModel
from apps.models.shop_model import ShellShopModel


class DishesCategoryModel(BaseModel):
    # 分类名
    name = db.Column(db.String(32), nullable=False)
    # 是否为默认选中
    is_default = db.Column(db.Boolean, default=False)
    # 分类描述
    description = db.Column(db.String(64), default="")
    # 分类编号
    type_accumulation = db.Column(db.String(32))
    # 外键,关联店铺主键
    shop_id = db.Column(db.Integer,db.ForeignKey(ShellShopModel.id))
    # 建立外键关系关系
    shop = db.relationship("ShellShopModel", backref="dishes")

    def keys(self):
        return "name","description","type_accumulation","is_default"
