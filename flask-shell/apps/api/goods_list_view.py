from apps.api import api_bp
from apps.models.shop_model import ShellShopModel
from flask import jsonify, request

# 店铺展示
@api_bp.route("/shop_list/", endpoint="shop_list", methods=["GET"])
def show_goods_list():
    shop = ShellShopModel.query.all()
    list = [dict(i, **{"id": i.pub_id}) for i in shop]
    return jsonify(list)

# 商品展示
@api_bp.route("/shop/", endpoint="shop", methods=["GET"])
def show_goods():
    shop_pubid = request.args.get("id")
    # shop = ShellShopModel.query.filter_by(pub_id=shop_pubid).first()
    shop1 = ShellShopModel.query.filter_by(pub_id=shop_pubid).all()
    data = [dict(dict(i), **{"commodity": [dict(dict(x), **{"goods_list": [dict(z) for z in x.info]}) for x in i.dishes]}) for i in shop1]
    data1 = data[0]
    return jsonify(data1)


