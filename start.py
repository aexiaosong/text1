from flask import Flask, render_template, request, redirect, url_for, session, g
from decorators import login_required
import config
from models import User, Water, Answer
from exts import db
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 主页函数
@app.route('/')
def index():
    context = {
        # 'waters': Water.query.order_by('-create_time').all()
        'waters': Water.query.order_by(Water.create_time.desc()).all() # 倒序查询
    }
    return render_template('index.html', **context)


# 登录函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return u'账号或密码输入错误，请确认后再输入！'


# 注册函数
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 方式验证，如果在数据库中查到就是已经注册过的
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该号码已经注册，请更换手机号码！'
        else:
            # 验证2次密码输入是否一致
            if password != password2:
                return u'两次密码输入不相等，请核对密码'
            else:
                user = User(telephone=telephone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


# 说话函数
@app.route('/talk/', methods=['GET', 'POST'])
@login_required
def talk():
    if request.method == 'GET':
        return render_template('talk.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        water = Water(title=title, content=content)
        # 获取当前用户
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()

        water.author = g.user
        db.session.add(water)
        db.session.commit()
        return redirect(url_for('index'))


# 详情页面
@app.route('/detail/<water_id>/')
def detail(water_id):
    water_model = Water.query.filter(Water.id == water_id).first()
    return render_template('detail.html', water=water_model)


# 评论函数
@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content') # 从form表单获取内容
    water_id = request.form.get('water_id') # 从form表单获取当前水流的id

    answer = Answer(content=content) # 创建一个答案对象，并把答案的内容写入对象

    # user_id = session['user_id'] # 从session中获取用户id
    # user = User.query.filter(User.id == user_id).first() # 从数据库中查询当前session中的用户

    answer.author = g.user # 把当前用户写到答案的作者上
    water = Water.query.filter(Water.id == water_id).first() # 从数据库中查询与当前水流对应的第一条数据
    answer.water = water # 把水流的信息记录到答案中
    db.session.add(answer) # 把答案对象添加到数据库中
    db.session.commit() # 执行数据库命令
    return redirect(url_for('detail', water_id=water_id))


# 查找函数
@app.route('/search/', methods=['GET'])
def search():
    q = ''
    q = request.args.get('q')
    # title,content
    # 或
    condition = or_(Water.title.contains(q), Water.content.contains(q))
    waters = Water.query.filter(condition).order_by(Water.create_time.desc()).all()
    # 与
    # waters = Water.query.filter(Water.title.contains(q),Water.content.contains(q))
    return render_template('index.html',waters=waters)


# 登出函数
@app.route('/logout/')
def logout():
    # 删除session
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('index'))


# 钩子函数
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


# 上下文函数
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
