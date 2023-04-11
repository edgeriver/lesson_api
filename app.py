from flask import Blueprint, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
# 定义蓝图flask_sqlalchemy
api = Blueprint("api", __name__)


# 在蓝图上定义路由
@api.route("/")
def index():
    return "Hello from API"


@api.route("/data")
def data():
    # 返回 JSON 格式数据
    return jsonify({"name": "John", "age": 25})


@api.route('/user')
def index2():
    # 查询所有用户
    users = User.query.all()

    # 将用户信息转换成字典列表
    users_list = [user.to_dict() for user in users]

    # 将结果返回为JSON格式
    return jsonify(users_list)


@api.route('/user2',endpoint='ttt')
def index2():
    # 查询所有用户
    engine = create_engine('mysql+pymysql://root:example@localhost/mydatabase')
    conn = engine.connect()

    # 执行查询并获取所有结果
    result = conn.execute(text('''SELECT * FROM user'''))
    column_name=tuple(result.keys())
    users_list=[dict(zip(column_name,tuple(i))) for i in result]
        # 将结果返回为JSON格式
    return jsonify(users_list)


@api.route('/init')
def init_db():
    # 查询所有用户
    db.create_all()
    return '数据库初始化成功'


# 在应用程序中注册蓝图
app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
# 设置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy
db = SQLAlchemy(app)


# 定义数据模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


if __name__ == "__main__":
    app.run()
