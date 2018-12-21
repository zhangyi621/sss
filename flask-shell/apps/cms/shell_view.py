from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user

from apps.forms.ShellForm import ShellRegisterForm, ShellLoginForm
from apps.models import db
from apps.cms import cms_bp

# 注册路由信息
from apps.models.login_model import ShellModel


@cms_bp.route("/index/", endpoint="index")
def shell_index():
    return render_template("cms/index.html")


# 登录
@cms_bp.route("/login/", endpoint="login", methods=["GET", "POST"])
def shell_login():
    form = ShellLoginForm(request.form)
    if request.method == "POST" and form.validate():
        # 数据库操作
        username = form.data.get("username")
        password = form.data.get("password")
        data = ShellModel.query.filter_by(username=username).first()
        if data and data.check_password(password):
            login_user(data)
            next_url = request.args.get("next", '')
            if not next_url.startswith("/"):
                next_url = None
            return redirect(next_url or url_for("cms.index"))
        form.password.errors = ["用户名或密码错误"]
    return render_template("cms/reg_login.html", form=form, flags="登录")


# 注册
@cms_bp.route("/register/", endpoint="register", methods=["GET", "POST"])
def shell_register():
    form = ShellRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        # 数据库操作
        print("...")
        s1 = ShellModel()
        s1.set_attrs(form.data)
        db.session.add(s1)
        db.session.commit()
        return redirect(url_for("cms.login"))
    return render_template("cms/reg_login.html", form=form, flags="注册")


# 注销
@cms_bp.route("/loginout/", endpoint="logout")
def shell_logout():
    logout_user()
    return redirect(url_for("cms.login"))

