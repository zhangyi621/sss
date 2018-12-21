from wtforms import Form, validators
from wtforms import StringField, BooleanField, SelectField


class CategoryForm(Form):
    name = StringField(label="菜品分类名", validators=[validators.DataRequired(message="必填项"),
                                                  validators.Length(max=16, message="名字最长16位")
                                                  ],
                       render_kw={"class": "form-control", "placeholder": "菜品分类名"}
                       )
    description = StringField(label="菜品描述",
                              render_kw={"class": "form-control", "placeholder": "菜品分类名"}
                              )
    type_accumulation = StringField(label="菜品分类编号", validators=[validators.DataRequired(message="必填项")],
                                    render_kw={"class": "form-control", "placeholder": "菜品分类名"}
                                    )
    is_default = BooleanField(label="是否默认")
    shop_id = SelectField(label="归属店铺", coerce=int, render_kw={"class": "form-control"}
                          )

    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.shop_id.choices = [(i.id, i.shop_name) for i in user.shop]
