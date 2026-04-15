from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from decimal import Decimal

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False  # 解决中文乱码

# 数据库连接
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",           
        password="hst20050429",          
        database="cat shop",   
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# ==========================
# 1. 注册接口
# ==========================
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "msg": "未接收到数据"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"code": 400, "msg": "用户名或密码不能为空"}), 400

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone()

        if exists:
            cursor.close()
            db.close()
            return jsonify({"code": 400, "msg": "用户名已存在"}), 400

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        db.commit()

        cursor.close()
        db.close()
        return jsonify({"code": 200, "msg": "注册成功"})

    except Exception as e:
        return jsonify({"code": 500, "msg": f"注册失败：{str(e)}"}), 500

# ==========================
# 2. 数据库测试接口
# ==========================
@app.route("/api/test-db", methods=["GET"])
def test_db():
    try:
        db = get_db_connection()
        db.close()
        return jsonify({"code": 200, "msg": "数据库连接成功 ✅"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"数据库连接失败 ❌：{str(e)}"}), 500

# ==========================
# 3. 登录接口
# ==========================
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user:
            return jsonify({"code": 401, "msg": "用户名或密码错误"})

        # 处理Decimal（如果有）
        for k, v in user.items():
            if isinstance(v, Decimal):
                user[k] = float(v)

        return jsonify({"code": 200, "msg": "登录成功", "data": user})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}"}), 500

# ==========================
# 4. 获取商品列表（最终修复版）
# ==========================
@app.route("/api/goods", methods=["GET"])
def get_goods():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM goods")
        goods = cursor.fetchall()
        cursor.close()
        db.close()

        # 把Decimal类型的price转为float
        for item in goods:
            if isinstance(item["price"], Decimal):
                item["price"] = float(item["price"])

        # 只传字典，不额外传default参数，彻底解决报错
        return jsonify({"code": 200, "data": goods})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"获取商品失败：{str(e)}"}), 500

# ==========================
# 5. 加入购物车（核心修复：补全count字段）
# ==========================
@app.route("/api/cart/add", methods=["POST"])
def add_cart():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        goods_id = data.get("goods_id")
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, count FROM cart WHERE user_id = %s AND goods_id = %s", (user_id, goods_id))
        item = cursor.fetchone()
        if item:
            cursor.execute("UPDATE cart SET count = count + 1 WHERE id = %s", (item["id"],))
        else:
            # 修复点：插入时添加count字段，默认值1
            cursor.execute("INSERT INTO cart (user_id, goods_id, count) VALUES (%s, %s, 1)", (user_id, goods_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"code": 200, "msg": "加入购物车成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"添加失败：{str(e)}"}), 500

# ==========================
# 6. 获取购物车列表（同步修复）
# ==========================
@app.route("/api/cart/list", methods=["POST"])
def cart_list():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            SELECT c.id, g.name, g.price, g.img_url, c.count
            FROM cart c
            LEFT JOIN goods g ON c.goods_id = g.id
            WHERE c.user_id = %s
        ''', (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        db.close()

        # 处理Decimal类型
        for item in cart_items:
            if isinstance(item["price"], Decimal):
                item["price"] = float(item["price"])

        return jsonify({"code": 200, "data": cart_items})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"获取失败：{str(e)}"}), 500

# ==========================
# 7. 修改购物车数量
# ==========================
@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    try:
        data = request.get_json()
        cart_id = data.get("cart_id")
        count = data.get("count")
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE cart SET count = %s WHERE id = %s", (count, cart_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"code": 200, "msg": "修改成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"修改失败：{str(e)}"}), 500

# ==========================
# 8. 删除购物车商品
# ==========================
@app.route("/api/cart/delete", methods=["POST"])
def delete_cart():
    try:
        data = request.get_json()
        cart_id = data.get("cart_id")
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"code": 200, "msg": "删除成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"删除失败：{str(e)}"}), 500

# ==========================
# 启动后端服务
# ==========================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)