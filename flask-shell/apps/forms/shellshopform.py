from wtforms import Form, StringField, validators
from wtforms import BooleanField, FloatField, FileField
from wtforms.widgets import HiddenInput


class ShopForm(Form):
    shop_name = StringField(label="店铺名称", validators=[validators.DataRequired(message="必填项"),
                                                      validators.Length(max=20, message="名称过长")
                                                      ],
                            render_kw={"class": "form-control", "placeholder": "店铺名称"}
                            )
    brand = BooleanField(label="品牌", default=False)
    on_time = BooleanField(label="准时送达", default=False)
    fengniao = BooleanField(label="蜂鸟配送", default=False)
    bao = BooleanField(label="保险", default=False)
    fapiao = BooleanField(label="发票", default=False)
    zhun = BooleanField(label="准标识", default=False)
    start_send = FloatField(label="起送价格", validators=[validators.DataRequired(message="必填项")
                                                      ],
                            render_kw={"class": "form-control", "placeholder": "起送价格"}
                            )
    send_cost = FloatField(label="配送费", validators=[validators.DataRequired(message="必填项")
                                                    ],
                           render_kw={"class": "form-control", "placeholder": "配送费"}
                           )
    notice = StringField(label="店铺公告", validators=[validators.DataRequired(message="必填项")],
                         render_kw={"class": "form-control", "placeholder": "店铺公告"}
                         )
    discount = StringField(label="优惠信息", validators=[validators.DataRequired(message="必填项")],
                           render_kw={"class": "form-control", "placeholder": "优惠信息"}
                           )
    shop_img = StringField(label="店铺图片",id="image-input",
                           render_kw={"class": "form-control"},
                           widget=HiddenInput())
