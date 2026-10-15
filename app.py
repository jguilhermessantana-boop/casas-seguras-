from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="casa_segura"
    )

tabelas = {
    "morador": ["nome", "telefone"],
    "sensor": ["tipo", "localizacao", "status"],
    "deteccao": ["id_sensor", "descricao"],
    "alerta": ["id_morador", "id_deteccao", "mensagem", "status"]
}

@app.route("/")
def inicio():
    return render_template("index.html", tabelas=tabelas)

@app.route("/<tabela>")
def listar(tabela):
    if tabela not in tabelas:
        return "Tabela não encontrada", 404

    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {tabela}")
    dados = cursor.fetchall()
    cursor.close()
    banco.close()

    return render_template(
        "index.html",
        tabelas=tabelas,
        dados=dados,
        tabela_atual=tabela
    )

@app.route("/cadastrar/<tabela>", methods=["POST"])
def cadastrar(tabela):
    if tabela not in tabelas:
        return "Tabela não encontrada", 404

    campos = tabelas[tabela]
    valores = [request.form[campo] for campo in campos]
    nomes = ", ".join(campos)
    marcas = ", ".join(["%s"] * len(campos))

    banco = conectar()
    cursor = banco.cursor()

    try:
        cursor.execute(
            f"INSERT INTO {tabela} ({nomes}) VALUES ({marcas})",
            valores
        )
        banco.commit()
    except mysql.connector.Error as erro:
        banco.rollback()
        cursor.close()
        banco.close()
        return f"Erro ao cadastrar: {erro}", 400

    cursor.close()
    banco.close()
    return redirect(f"/{tabela}")

@app.route("/editar/<tabela>/<int:id>", methods=["POST"])
def editar(tabela, id):
    if tabela not in tabelas:
        return "Tabela não encontrada", 404

    campos = tabelas[tabela]
    valores = [request.form[campo] for campo in campos]
    alteracoes = ", ".join(
        [f"{campo} = %s" for campo in campos]
    )

    banco = conectar()
    cursor = banco.cursor()

    try:
        cursor.execute(
            f"UPDATE {tabela} SET {alteracoes} WHERE id = %s",
            valores + [id]
        )
        banco.commit()
    except mysql.connector.Error as erro:
        banco.rollback()
        cursor.close()
        banco.close()
        return f"Erro ao editar: {erro}", 400

    cursor.close()
    banco.close()
    return redirect(f"/{tabela}")

@app.route("/excluir/<tabela>/<int:id>", methods=["POST"])
def excluir(tabela, id):
    if tabela not in tabelas:
        return "Tabela não encontrada", 404

    banco = conectar()
    cursor = banco.cursor()

    try:
        cursor.execute(
            f"DELETE FROM {tabela} WHERE id = %s",
            (id,)
        )
        banco.commit()
    except mysql.connector.Error:
        banco.rollback()
        cursor.close()
        banco.close()
        return "Não foi possível excluir. Este registro pode estar relacionado a outro.", 400

    cursor.close()
    banco.close()
    return redirect(f"/{tabela}")

if __name__ == "__main__":
    app.run(debug=True)
