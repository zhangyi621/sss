from wtforms import Form, validators, SelectField
from wtforms import StringField, FloatField, IntegerField
from wtforms.widgets import HiddenInput


class InfoForm(Form):
    goods_name = StringField(label="菜品名", validators=[validators.DataRequired(message="必填项")],
                             render_kw={"class": "form-control", "placeholder": "菜品名称"}
                             )
    cate_id = SelectField(label="菜品分类", coerce=int, render_kw={"class": "form-control"}
                          )
    goods_price = FloatField(label="菜品价格", validators=[validators.DataRequired(message="必填项")],
                             render_kw={"class": "form-control", "placeholder": "菜品信息"}
                             )
    tips = StringField(label="菜品提示信息", render_kw={"class": "form-control", "placeholder": "菜品提示信息"})
    description = StringField(label="菜品描述", render_kw={"class": "form-control", "placeholder": "菜品描述"})
    goods_img = StringField(label="店铺图片", id="image-input",
                            render_kw={"class": "form-control"},
                            widget=HiddenInput())

    def __init__(self, shop, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.cate_id.choices = [(i.id, i.name) for i in shop.dishes]
