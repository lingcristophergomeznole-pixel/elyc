# server.py — Sistema de Prensa Católica ELYC (Entre Luces y Cámara)
from flask import Flask, request, redirect, session
import sqlite3, hashlib, os

app = Flask(__name__)
app.secret_key = "clave_secreta_segura_elyc"

DB_NAME = "elyc.db"

# 🧱 Crear la base de datos si no existe
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Tabla de administrador
        c.execute("""
            CREATE TABLE admin (
                usuario TEXT PRIMARY KEY,
                clave TEXT
            )
        """)

        # Tabla de noticias
        c.execute("""
            CREATE TABLE noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                contenido TEXT
            )
        """)

        # Insertar usuario admin por defecto (usuario: admin / contraseña: 1234)
        c.execute("INSERT INTO admin VALUES (?, ?)",
                  ("admin", hashlib.sha256("1234".encode()).hexdigest()))
        conn.commit()
        conn.close()
        print("✅ Base de datos creada correctamente: elyc.db")

# 🔐 Ruta de inicio
@app.route("/")
def index():
    return redirect("/noticias")

# 📰 Ver noticias (público)
@app.route("/noticias")
def noticias():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT titulo, contenido FROM noticias ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    html = """
    <html><head><meta charset='utf-8'><title>Noticias - ELYC</title></head>
    <body style='font-family:Poppins;background:#4b0082;color:white;padding:20px;'>
    <h1>📰 Noticias - Entre Luces y Cámara</h1>
    """
    for t, ctt in data:
        html += f"<article style='background:#fff2;border-radius:10px;padding:15px;margin:10px 0;'><h2>{t}</h2><p>{ctt}</p></article>"
    html += "<br><a href='/login' style='color:gold;'>🔑 Acceso administrador</a></body></html>"
    return html

# 🔑 Login del administrador
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = hashlib.sha256(request.form["clave"].encode()).hexdigest()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE usuario=? AND clave=?", (usuario, clave))
        user = c.fetchone()
        conn.close()
        if user:
            session["admin"] = True
            return redirect("/admin")
        else:
            return "<h3 style='color:red;'>❌ Usuario o contraseña incorrectos</h3><a href='/login'>Volver</a>"

    return """
    <html><head><meta charset='utf-8'><title>Login ELYC</title></head>
    <body style='font-family:Poppins;background:#4b0082;color:white;text-align:center;padding:40px;'>
      <h2>🔒 Ingreso del Administrador</h2>
      <form method='POST'>
        <input name='usuario' placeholder='Usuario' required style='padding:8px;border-radius:6px;'><br><br>
        <input name='clave' type='password' placeholder='Contraseña' required style='padding:8px;border-radius:6px;'><br><br>
        <button style='padding:10px 20px;background:gold;border:none;border-radius:8px;'>Entrar</button>
      </form>
    </body></html>
    """

# 📋 Panel de administración
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, titulo, contenido FROM noticias ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    html = """
    <html><head><meta charset='utf-8'><title>Admin ELYC</title></head>
    <body style='font-family:Poppins;background:#4b0082;color:white;padding:20px;'>
    <h1>📋 Panel de Administración - ELYC</h1>
    <form method='POST' action='/agregar'>
      <input name='titulo' placeholder='Título' required style='width:80%;padding:8px;border-radius:6px;'><br><br>
      <textarea name='contenido' placeholder='Contenido...' required style='width:80%;height:100px;border-radius:6px;'></textarea><br><br>
      <button style='padding:10px 20px;background:gold;border:none;border-radius:8px;'>Agregar noticia</button>
    </form>
    <hr>
    <h2>🗞 Noticias existentes</h2>
    """
    for n in data:
        html += f"<div style='background:#fff2;padding:10px;border-radius:10px;margin:8px 0;'><h3>{n[1]}</h3><p>{n[2]}</p><a href='/eliminar/{n[0]}' style='color:red;'>🗑 Eliminar</a></div>"
    html += "<br><a href='/logout' style='color:gold;'>🚪 Cerrar sesión</a></body></html>"
    return html

# ➕ Agregar noticia
@app.route("/agregar", methods=["POST"])
def agregar():
    if not session.get("admin"):
        return redirect("/login")

    titulo = request.form["titulo"]
    contenido = request.form["contenido"]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO noticias (titulo, contenido) VALUES (?,?)", (titulo, contenido))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ❌ Eliminar noticia
@app.route("/eliminar/<int:id>")
def eliminar(id):
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM noticias WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# 🚪 Cerrar sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# 🧩 Iniciar
if __name__ == "__main__":
    init_db()
    app.run(debug=True)