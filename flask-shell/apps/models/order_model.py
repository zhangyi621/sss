from apps.models import BaseModel, db


class OrderGoodsModel(BaseModel):
    order_id = db.Column(db.Integer, db.ForeignKey('buyer_order.id'))
    # 商品ID号
    goods_id = db.Column(db.Integer)
    # 商品名称
    goods_name = db.Column(db.String(64))
    # 商品图片
    goods_img = db.Column(db.String(128), default='')
    # 商品价钱
    goods_price = db.Column(db.Float)
    # 商品数量
    amount = db.Column(db.Integer)

    order = db.relationship('BuyerOrder', backref='goods')

    def keys(self):
        return "goods_id", "goods_name", "goods_img", "goods_price", "amount"
