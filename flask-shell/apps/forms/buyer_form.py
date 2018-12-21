from wtforms import Form, StringField, validators, ValidationError, IntegerField
import redis


class BuyerRegisterForm(Form):
    username = StringField(label="用户名", validators=[validators.DataRequired(message="必填项"),
                                                    validators.Length(max=16, message="用户名过长")
                                                    ]
                           )
    tel = StringField(label="密码", validators=[validators.DataRequired(message="必填项"),
                                              validators.Regexp(r"1[3-9][0-9]{9}", message="手机号码格式错误")
                                              ])
    password = StringField(label="密码", validators=[validators.DataRequired(message="必填项")
                                                   ])
    sms = StringField(label="验证码", validators=[validators.DataRequired("必填项")])

    # pwd = StringField(label="确认密码", validators=[validators.EqualTo("password", message="输入密码不一致")])

    def validate_sms(self, sms):
        r = redis.StrictRedis(host="192.168.136.128", port=6390)
        rsms = r.get(self.tel.data)
        if not rsms and rsms.decode("utf-8") != sms.data:
            raise ValidationError("验证码错误")


class BuyerLoginForm(Form):
    name = StringField(label="用户名", validators=[validators.DataRequired(message="必填项"),
                                                validators.Length(max=16, message="用户名过长")
                                                ])
    password = StringField(label="密码", validators=[validators.DataRequired(message="必填项")
                                                   ])


class BuyerAddressForm(Form):
    id = IntegerField(default=0)
    provence = StringField(label="省", validators=[validators.DataRequired(message="必填项"),
                                                  validators.Length(max=32, message="省的名称过长")
                                                  ]
                           )
    city = StringField(label="市", validators=[validators.DataRequired(message="必填项"),
                                              validators.Length(max=32, message="省的名称过长")]
                       )
    # 县
    area = StringField(label="县/区", validators=[validators.DataRequired(message="必填项"),
                                                validators.Length(max=32, message="省的名称过长")])
    # 详细地
    detail_address = StringField(label="详细地址", validators=[validators.DataRequired(message="必填项")])
    # 收货人
    name = StringField(label="收货人姓名", validators=[validators.DataRequired(message="必填项")])
    # 收货人
    tel = StringField(label="收货人电话", validators=[validators.DataRequired(message="必填项"),
                                                 validators.Regexp(
                                                     r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
                                                     r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码"),
                                                 ],
                      )
