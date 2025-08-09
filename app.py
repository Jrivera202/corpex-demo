import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devsecret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///corpex_demo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(200))
    monto = db.Column(db.Float)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(200))
    monto = db.Column(db.Float)

# ✅ Flask 3: Crear la base de datos al iniciar la app
with app.app_context():
    db.create_all()

USERS = {
    "agencia1": "demo123"
}

# ✅ Decorador corregido con wraps para evitar errores
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/", methods=["GET"])
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    ventas_total = db.session.query(db.func.coalesce(db.func.sum(Venta.monto), 0)).scalar()
    gastos_total = db.session.query(db.func.coalesce(db.func.sum(Gasto.monto), 0)).scalar()
    balance = ventas_total - gastos_total
    return render_template("dashboard.html", ventas_total=ventas_total, gastos_total=gastos_total, balance=balance)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        if user in USERS and USERS[user] == password:
            session["user"] = user
            return redirect(url_for("index"))
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/ventas", methods=["GET", "POST"])
@login_required
def ventas():
    if request.method == "POST":
        desc = request.form.get("descripcion")
        monto = request.form.get("monto")
        try:
            monto = float(monto)
            db.session.add(Venta(descripcion=desc, monto=monto))
            db.session.commit()
            flash("Venta registrada", "ok")
        except Exception as e:
            db.session.rollback()
            flash("Error: " + str(e), "error")
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("ventas.html", ventas=ventas)

@app.route("/gastos", methods=["GET", "POST"])
@login_required
def gastos():
    if request.method == "POST":
        desc = request.form.get("descripcion")
        monto = request.form.get("monto")
        try:
            monto = float(monto)
            db.session.add(Gasto(descripcion=desc, monto=monto))
            db.session.commit()
            flash("Gasto registrado", "ok")
        except Exception as e:
            db.session.rollback()
            flash("Error: " + str(e), "error")
    gastos = Gasto.query.order_by(Gasto.fecha.desc()).all()
    return render_template("gastos.html", gastos=gastos)

@app.route("/reportes")
@login_required
def reportes():
    ventas_total = db.session.query(db.func.coalesce(db.func.sum(Venta.monto), 0)).scalar()
    gastos_total = db.session.query(db.func.coalesce(db.func.sum(Gasto.monto), 0)).scalar()
    balance = ventas_total - gastos_total
    return render_template("reportes.html", ventas_total=ventas_total, gastos_total=gastos_total, balance=balance)

if _name_ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
