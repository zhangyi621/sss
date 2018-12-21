import uuid

# 生成uuid
import redis
from flask import request, jsonify, g
from apps.models.todo_user import BuyerUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 店铺pid
def shop_pid():
    data = str(uuid.uuid4())
    return "".join(data.split("-")[:3])


# 验证token的生成器
def login_token(fn):
    def newfn(*args, **kwargs):
        # 验证请求字段是否含有token
        token = request.cookies.get("token")
        if not token:
            return jsonify({"status": 401, "message": "用户未登录"})
        # 查询数据库
        s = Serializer(secret_key="elm_api", expires_in=500)
        uid = s.loads(token).get("uid")
        user = BuyerUser.query.filter_by(id=uid).first()
        if not user:
            return jsonify({"status": 401, "message": "非法用户"})
        g.current_user = user
        ret = fn(*args, **kwargs)
        return ret

    return newfn


def client_redis(host="127.0.0.1", port=6390):
    r = redis.StrictRedis(host=host,port=port)
    return r