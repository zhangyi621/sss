from apps.models import db, BaseModel
from apps.models.dishes_category_model import DishesCategoryModel


class DishesInfoModel(BaseModel):
    goods_id = db.Column(db.String(16), index=True)
    goods_name = db.Column(db.String(32), nullable=False)
    goods_price = db.Column(db.Float, nullable=False)
    goods_img = db.Column(db.String(64))
    month_sales = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=5.0)
    tips = db.Column(db.String(64), default="")
    description = db.Column(db.String(64), default="")
    cate_id = db.Column(db.Integer, db.ForeignKey(DishesCategoryModel.id))
    cate = db.relationship("DishesCategoryModel", backref="info")

    def keys(self):
        return "goods_id", "goods_name", "goods_price", "goods_img", "month_sales", "rating", \
               "tips", "description",
