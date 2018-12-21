from flask_login import login_required, current_user

from apps.cms import cms_bp
from apps.models import db
from apps.models.dishes_category_model import DishesCategoryModel
from apps.models.shop_model import ShellShopModel
from flask import render_template, request, redirect, url_for
from apps.forms.dishescategoryform import CategoryForm


# 菜品风雷展示
@cms_bp.route("/category/<shop_id>/", endpoint="category", methods=["GET", "POST"])
@login_required
def dishes_category(shop_id):
    shop = ShellShopModel.query.filter_by(id=shop_id).first()
    cates = DishesCategoryModel.query.filter_by(shop_id=shop_id).all()
    return render_template("cms/show_cates.html", cates=cates, shop=shop)


@cms_bp.route("/cate1_add/<shop_id>/", endpoint="cate1_add", methods=["GET", "POST"])
@login_required
def dishes_add(shop_id):
    form = CategoryForm(request.form)
    if request.method == "POST" and form.validate():
        # 实例化数据模型类
        ca1 = DishesCategoryModel()
        ca1.set_attrs(request.form)
        ca1.shop_id = shop_id
        db.session.add(ca1)
        db.session.commit()
        return redirect(url_for("cms.category", shop_id=shop_id))
    return render_template("cms/add_cls.html", form=form, flags="添加菜品分类")


@cms_bp.route("/cate_add/", endpoint="cate_add", methods=["GET", "POST"])
@login_required
def dishes_add():
    form = CategoryForm(current_user, request.form)
    if request.method == "POST" and form.validate():
        # 实例化数据模型类
        ca1 = DishesCategoryModel()
        ca1.set_attrs(request.form)
        db.session.add(ca1)
        db.session.commit()
        return redirect(url_for("cms.category", shop_id=ca1.shop_id))
    return render_template("cms/add_cls.html", form=form, flags="添加菜品分类")
