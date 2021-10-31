from flask import Flask, json, request
from flask.templating import render_template
from flask_cors import CORS
from Analizador.gramatica import parser
from Analizador.Optimizacion import parser2
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Temporal import Temporal
import pydot

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/analizar", methods=['POST', 'GET'])
def start():
    data = request.get_json(force=True)

    input = data["text"]
    # obtener ruta
    ast = parser.parse(input)

    symbol_table = SymbolTable(None, 'Global')
    driver = Driver()
    driver.agregarTabla(symbol_table)
    ast.ejecutar(driver, symbol_table)
    print(driver.console)

    resp = {
        "text": driver.console
    }
    try:
        reps = reportes(ast, driver, symbol_table)
        resp += reps
    except:
        pass

    return json.jsonify(resp)


@app.route('/compilar', methods=['POST'])
def compilar():
    data = request.get_json(force=True)
    input = data["text"]

    ast = parser.parse(input)

    symbol_table = SymbolTable(None, 'Global')
    driver = Driver()
    driver.agregarTabla(symbol_table)
    temporal = Temporal()
    ast.compilar(driver, symbol_table, temporal)

    resp = {
        "text": driver.console
    }
    return json.jsonify(resp)


@app.route('/mirilla', methods=['POST'])
def mirilla():
    try:
        data = request.get_json(force=True)
        input = data["text"]

        instructions = parser2.parse(input)

        instructions.Mirilla()

        output = instructions.getCode()

        resp = {
            "text": output
        }
        return resp
    except:
        resp = {
            "text": input
        }
        return resp


def reportes(ast, driver, symbol_table):
    raiz = ast.traverse()
    dot_txt = raiz.GraficarSintactico()

    f = open('static/assets/err.html', 'w+')
    err = driver.graficar_er(driver, symbol_table)
    x = f.write(err)
    f.close()

    ts_file = open('static/assets/ts.html', 'w+')
    ts_t = driver.graficar_st(driver, symbol_table)
    y = ts_file.write(ts_t)
    ts_file.close()

    graph = pydot.graph_from_dot_data(dot_txt)
    graph[0].write_svg('static/assets/ast.svg')

    return {
        "text": driver.console,
        "err": err,
        "ts": ts_t,
        "graph": dot_txt
    }


if __name__ == "__main__":
    app.run()
