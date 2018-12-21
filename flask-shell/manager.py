from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps import create_app
from apps.models import db
from apps.settings import Devconfig

# 导入包,创建app
app = create_app(Devconfig)
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command("db", MigrateCommand)
if __name__ == '__main__':
    print(app.url_map)
    # 启动服务器
    app.run()
