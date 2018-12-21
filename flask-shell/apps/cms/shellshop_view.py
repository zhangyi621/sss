from flask import render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from qiniu import Auth

from apps.cms import cms_bp
from apps.forms.shellshopform import ShopForm
from apps.models import db
from apps.models.shop_model import ShellShopModel
from apps.libs.shop_setpid import shop_pid


@cms_bp.route("/shop_index/", endpoint="shop_index")
def shop_index():
    sess = session.get("user_id")
    stores = ShellShopModel.query.filter_by(seller_pid=sess).all()
    return render_template("cms/profile.html", stores=stores)


@cms_bp.route("/shop_add/", endpoint="shop_add", methods=["GET", "POST"])
@login_required
def shop_add():
    form = ShopForm(request.form)
    if request.method == "POST" and form.validate():
        sp1 = ShellShopModel()
        sp1.set_attrs(form.data)
        sp1.pub_id = shop_pid()
        sp1.seller_pid = current_user.id
        db.session.add(sp1)
        db.session.commit()
        return redirect(url_for("cms.shop_index"))
    return render_template("cms/add_cls.html", form=form, flags="店铺添加")


@cms_bp.route("/shop_update/<pub_id>/", endpoint="shop_update", methods=["GET", "POST"])
@login_required
def shop_update(pub_id):
    ob1 = ShellShopModel.query.filter_by(pub_id=pub_id).first()
    if not ob1:
        return "没有该店铺信息"
    if request.method == "POST":
        form = ShopForm(request.form)
        # 更新数据库
        if form.validate():
            ob1.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for("cms.shop_index"))
    else:
        # 回显数据
        form = ShopForm(data=dict(ob1))
    return render_template("cms/add_cls.html", form=form, flags="店铺更新")


@cms_bp.route("/uptoken/", endpoint="uptoken", methods=["GET","POST"])
def get_uptoken():
    AccessKey = "IRXBTG9EdiUr6RIG0OcTEW1IgnhjLoaTVHvgYjeX"
    SecretKey = "mhqfViFy8htQUbEF00_eGJ653qYoebm_FN9A0atY"
    q = Auth(access_key=AccessKey, secret_key=SecretKey)
    token = q.upload_token("flaskimg")
    return jsonify({"uptoken": token})
