from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_BASE = "http://localhost:5001"

# Vista principal: mostrar usuarios
@app.route("/", methods=["GET", "POST"])
def inicio():
    # Manejo de acciones de actualizar/eliminar desde la tabla
    if request.method == "POST":
        accion = request.form.get("accion")
        usuario = {
            "id": int(request.form.get("id")),
            "nombre": request.form.get("nombre"),
            "edad": int(request.form.get("edad"))
        }

        if accion == "actualizar":
            requests.put(f"{API_BASE}/v1/usuarios/", json=usuario)
        elif accion == "eliminar":
            requests.delete(f"{API_BASE}/v1/usuarios/", json=usuario)

        return redirect(url_for("inicio"))

    # Consultar todos los usuarios
    try:
        res = requests.get(f"{API_BASE}/V1/Usuarios/")
        if res.status_code == 200:
            usuarios = res.json().get("Usuarios", [])
        else:
            usuarios = []
    except:
        usuarios = []

    return render_template("index.html", usuarios=usuarios)


# Vista para crear usuario
@app.route("/crear", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        usuario = {
            "id": int(request.form.get("id")),
            "nombre": request.form.get("nombre"),
            "edad": int(request.form.get("edad"))
        }
        requests.post(f"{API_BASE}/v1/usuarios/", json=usuario)
        return redirect(url_for("inicio"))

    return render_template("crear.html")


if __name__ == "__main__":
    app.run(debug=True)
