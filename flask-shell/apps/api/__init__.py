from flask import Blueprint


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

from apps.api import goods_list_view
from apps.api import user_login_view