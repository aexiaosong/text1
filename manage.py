from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from start import app
from exts import db
from models import User,Water

manager = Manager(app)

# 绑定Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# 迁移步骤
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade