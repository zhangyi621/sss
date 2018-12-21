from flask import Blueprint

# 创建蓝图对象
cms_bp = Blueprint("cms", __name__)

# 将视图注册到蓝图中
from apps.cms import shell_view
from apps.cms import shellshop_view
from apps.cms import dishes_view
from apps.cms import goods_info_view