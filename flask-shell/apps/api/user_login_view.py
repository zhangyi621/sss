import json
from datetime import datetime

from apps.api import api_bp
from flask import request, jsonify, g
import random
from apps.forms.buyer_form import BuyerRegisterForm, BuyerLoginForm, BuyerAddressForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import redis
from apps.libs.shop_setpid import login_token, client_redis, shop_pid
from apps.models import db
from apps.models.todo_user import BuyerUser, BuyerAddress, BuyerOrder
from apps.models.dishes_info_model import DishesInfoModel
from apps.models.order_model import OrderGoodsModel
from apps.models.shop_model import ShellShopModel


# 用户注册
@api_bp.route("/register/", endpoint="user_register", methods=["POST"])
def user_register():
    tel = request.form.get("tel")
    form = BuyerRegisterForm(request.form)
    r = redis.StrictRedis(host="192.168.136.128", port=6390)
    data = r.get(tel)
    print(data)
    print(request.form.get('sms'))
    if form.validate():
        u1 = BuyerUser()
        u1.set_attrs(form.data)
        db.session.add(u1)
        db.session.commit()
        return jsonify({"status": 200, "message": "注册成功"})
    return jsonify({"status": 401, "message": 'cw'.join(['{}:{}'.format(k, v[0]) for k, v in form.errors.items()])
                    })


# 验证码
@api_bp.route("/sms/", endpoint="user_sms", methods=["GET"])
def create_sms():
    tel = request.args.get("tel")
    if tel:
        sms = "".join([str(random.randint(0, 9)) for i in range(4)])
        r = redis.StrictRedis(host="192.168.136.128", port=6390)
        r.setex(tel, 1000, sms)
        print(sms)
        return jsonify({"status": 200, "message": "成功"})
    return jsonify({"status": 401, "message": "手机号码有误"})


# 登录信息
@api_bp.route("/login/", endpoint="user_login", methods=["POST"])
def users_login():
    data = request.form
    form = BuyerLoginForm(data)
    if form.validate():
        # 验证成功
        username = data.get("name")
        user = BuyerUser.query.filter_by(username=username).first()
        if not user or not user.check_password(data.get("password")):
            return jsonify({"status": 401, "message": "用户不存在或密码错误"})
        s = Serializer(secret_key="elm_api", expires_in=500)
        data1 = s.dumps({"uid": user.id})
        response = jsonify({"status": "true", "message": "登录成功", "user_id": user.id,
                            'username': user.username})
        response.set_cookie('token', data1.decode('ascii'))
        return response
    return jsonify({"status": 401, "message": "数据不合法"})


# 地址查看
@api_bp.route("/address/", endpoint="show_address", methods=["GET"])
@login_token
def show_address():
    id = request.args.get("id")
    if not id:
        # 展示所有地址
        addrs = g.current_user.addresses
        res = [dict(dict(i), **{"id": num + 1}) for num, i in enumerate(addrs)]
        return jsonify(res)
    else:
        addrs = g.current_user.addresses
        addr = dict(addrs[int(id) - 1])
        return jsonify(addr)


# 地址修改
@api_bp.route("/address/", endpoint="change_address", methods=["POST"])
@login_token
def create_address():
    form = BuyerAddressForm(request.form)
    if form.validate():
        if form.id.data:
            # form有id, 说明是修改地址
            addrs = g.current_user.addresses
            ad = addrs[form.data["id"] - 1]
            ad.set_attrs(form.data)
            message = "修改地址成功"
        else:
            # 没有id ,新添地址信息
            ad = BuyerAddress()
            ad.set_attrs(form.data)
            message = "添加地址成功"
            ad.user = g.current_user
        db.session.add(ad)
        db.session.commit()
        return jsonify({"status": "true", "message": message})
    return jsonify({"status": 'False', "message": "数据错误,请重新输入"})


# 购物车
@api_bp.route("/cart/", endpoint="add_cart", methods=["POST"])
@login_token
def add_cart():
    goods_id_list = request.form.getlist("goodsList[]")
    goods_count = request.form.getlist("goodsCount[]")
    res = zip(goods_id_list, goods_count)
    # 将数据保存在redis
    user_id = g.current_user.id
    redis = client_redis()
    redis.delete(user_id)
    for i in res:
        good = DishesInfoModel.query.filter_by(goods_id=i[0]).first()
        goods = dict(good)
        redis.hset(user_id, json.dumps(goods), i[1])
    return jsonify({"status": "true", "message": "添加成功"})


# 购物车展示
@api_bp.route("/cart/", endpoint="show_cart", methods=["GET"])
@login_token
def show_cart():
    user_id = g.current_user.id
    redis = client_redis()
    goods = redis.hkeys(user_id)
    list = []
    total = 0
    for i in goods:
        count = redis.hget(user_id, i).decode("utf-8")
        # print(count)
        good = json.loads(i)
        good["amount"] = count
        # print(good)
        total += good.get("goods_price") * int(count)
        list.append(good)
    return jsonify({"status": "true", "goods_list": list, "totalCost": total})


def mycreate(addr, user):
    user_id = user.id
    # code = shop_pid()
    redis = client_redis()
    goods = redis.hkeys(user_id)
    # list = []
    total = 0
    b1 = BuyerOrder()
    b1.user_id = user_id
    b1.order_code = shop_pid()
    b1.order_address = addr
    b1.order_tiem = datetime.now()
    for i in goods:
        count = redis.hget(user_id, i).decode("utf-8")
        # print(count)
        # 商品信息
        good = json.loads(i)
        # 订单数量
        good["amount"] = count
        # print(good)
        # 订单价格
        total += good.get("goods_price") * int(count)
        # list.append(good)
        good_obj = DishesInfoModel.query.filter_by(goods_id=good["goods_id"]).first()
        # 添加订单信息
        # 实例化订单类
        # 添加订单商品
        b1.shop_id = good_obj.cate.shop.id
        b1.order_price = total
        b1.goods.append(
            OrderGoodsModel(goods_id=good_obj.id, goods_name=good["goods_name"],
                            goods_img=good["goods_img"], goods_price=good["goods_price"],
                            amount=int(good['amount']))
        )
    db.session.add(b1)
    db.session.commit()
    return b1


# 生成订单
@api_bp.route("/order/", endpoint="show_order", methods=["POST"])
@login_token
def order_add():
    address = int(request.form.get("address_id"))
    ad1 = BuyerAddress.query.filter_by(id=address).first()
    str_addr = ad1.provence + ad1.city + ad1.area + ad1.detail_address
    # 添加订单商品
    user = g.current_user
    order = mycreate(addr=str_addr, user=user)
    return jsonify({"status": "true", "message": "订单已生成", "order_id": order.order_code})


# 查看订单详情
@api_bp.route("/order/", endpoint="show_order1", methods=["GET"])
@login_token
def create_show():
    order_code = request.args.get("id")
    order = BuyerOrder.query.filter_by(order_code=order_code).first()
    order_goods = order.goods
    list = [dict(i) for i in order_goods]
    shop = ShellShopModel.query.filter_by(id=order.shop_id).first()
    data = {
        **dict(order),
        'id': order.id,
        'order_status': order.get_status(),
        'goods_list': list,
        'order_birth_time': order.order_tiem.strftime("%Y-%m-%d %H:%M"),
        'shop_name': shop.shop_name,
        'shop_img': shop.shop_img,
    }
    return jsonify(data)


# 查看所有订单
@api_bp.route("/orders/", endpoint="orders", methods=["GET"])
@login_token
def get_orders():
    # 获得所有订单详情
    user = g.current_user
    orders = user.order
    data = [{
        "id": order.order_code,
        "order_birth_time": order.order_tiem.strftime("%Y-%m-%d %H:%M"),
        **dict(order),
        "shop_name": order.shop.shop_name,
        "shop_img": order.shop.shop_img,
        "goods_list": [dict(x) for x in order.goods],
        "order_status": order.get_status(),
    } for order in orders]
    return jsonify(data)
