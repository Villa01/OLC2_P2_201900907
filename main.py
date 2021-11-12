import os

from flask import Flask, json, request
from flask.templating import render_template
from flask_cors import CORS
from Structure.SymbolTable.SymbolTable import SymbolTable
from Structure.Driver import Driver
from Temporal import Temporal
import pydot

from Analizador.Compilar import gramatica
from Analizador.Optimizacion import Optimizacion

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
    ast = gramatica.parser.parse(input)

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

    ast = gramatica.parser.parse(input)

    symbol_table = SymbolTable(None, 'Global')
    driver = Driver()
    driver.agregarTabla(symbol_table)
    temporal = Temporal()
    ast.compilar(driver, symbol_table, temporal)

    # reportes(ast, driver, symbol_table)

    resp = {
        "text": driver.console
    }
    return json.jsonify(resp)


optimizador = None


@app.route('/reportes', methods=['POST'])
def rep():
    data = request.get_json(force=True)
    input = data["text"]

    ast = gramatica.parser.parse(input)

    symbol_table = SymbolTable(None, 'Global')
    driver = Driver()
    driver.agregarTabla(symbol_table)
    temporal = Temporal()
    ast.compilar(driver, symbol_table, temporal)

    reportes(ast, driver, symbol_table)

    resp = {
        "status": 200
    }
    return json.jsonify(resp)


@app.route('/mirilla', methods=['POST'])
def mirilla():
    data = request.get_json(force=True)
    input = data["text"]

    instructions = Optimizacion.parser2.parse(input)

    global optimizador
    optimizador = instructions

    instructions.Mirilla()

    output = instructions.getCode()

    resp = {
        "text": output
    }
    return resp


@app.route('/bloques', methods=['POST'])
def bloques():
    try:
        data = request.get_json(force=True)
        input = data["text"]
        global optimizador
        optimizador = Optimizacion.parser2.parse(input)

        resp = {
            "text": input
        }
        return resp
    except:
        resp = {
            "text": input
        }
        return resp


def reportes(ast, driver, symbol_table):
    #raiz = ast.traverse()
    #dot_txt = raiz.GraficarSintactico()


    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets', 'err.html')
    f = open(path, 'w+')
    err = driver.graficar_er(driver, symbol_table)
    x = f.write(err)
    f.close()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets', 'ts.html')
    ts_file = open(path, 'w+')
    ts_t = driver.graficar_st(driver, symbol_table)
    y = ts_file.write(ts_t)
    ts_file.close()

    if optimizador:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets', 'optimizacion.html')
        ts_file = open(path, 'w+')
        op_t = optimizador.generar_reporte()
        y = ts_file.write(op_t)
        ts_file.close()

    #path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets', 'ast.svg')
    #graph = pydot.graph_from_dot_data(dot_txt)
    #graph[0].write_svg(path)

    return {
        "text": driver.console,
        "err": err,
        "ts": ts_t,
        #"graph": dot_txt
    }


if __name__ == "__main__":
    app.run()
