from apps.cms import cms_bp
from flask import request, redirect, render_template, url_for
from flask_login import login_required

from apps.models import db
from apps.models.shop_model import ShellShopModel
from apps.models.dishes_info_model import DishesInfoModel
from apps.forms.goodsinfoform import InfoForm
from apps.libs.shop_setpid import shop_pid


# 菜品首页
@cms_bp.route("/info_index/<shop_id>/", endpoint="info_index")
@login_required
def show_goods_info(shop_id):
    shop = ShellShopModel.query.filter_by(id=shop_id).first()  # 单个店铺对象
    # 根据单个店铺对象获得该店铺下的所有菜品分类集合
    cate = shop.dishes
    items = [[i.name, i.info] for i in cate]
    return render_template("cms/show_foods.html", items=items, shop=shop)


# 添加菜品
@cms_bp.route("/info_add/<shop_id>/", endpoint="info_add", methods=["GET", "POST"])
@login_required
def add_goods(shop_id):
    # 得到商铺对象
    shop = ShellShopModel.query.filter_by(id=shop_id).first()
    # 初始化form
    form = InfoForm(shop, request.form)
    if request.method == "POST" and form.validate():
        # 得到菜品信息数据模型对象
        n1 = DishesInfoModel()
        n1.set_attrs(form.data)
        n1.goods_id = shop_pid()
        db.session.add(n1)
        db.session.commit()
        return redirect(url_for("cms.info_index",shop_id=shop_id))
    return render_template("cms/add_cls.html", form=form, flags="菜品添加")


# 菜品更新
@cms_bp.route("/info_update/<shop_id>/<info_id>/", endpoint="info_update", methods=["GET", "POST"])
@login_required
def goods_info_update(shop_id, info_id):
    # 得到菜品信息对象
    info = DishesInfoModel.query.filter_by(id=info_id).first()
    shop = ShellShopModel.query.filter_by(id=shop_id).first()
    if not info:
        return "没有该菜品"
    form = InfoForm(shop, request.form)
    if request.method == "POST":
        if form.validate():
            info.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for("cms.info_index",shop_id=shop.id))
    form = InfoForm(shop, data=dict(info))
    return render_template("cms/add_cls.html", form=form, flags="菜品更新")
