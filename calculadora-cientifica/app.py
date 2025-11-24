import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from flask import Flask, render_template, request
import math

app = Flask(__name__)

def try_float(x):
    try:
        if x is None:
            return None
        x = str(x).replace(',', '.')
        return float(x)
    except:
        return None

def format_number(n):
    if n % 1 == 0:
        return str(int(n))
    else:
        return f"{round(n, 2)}"

def plot_func(x_vals, y_vals, title="Gráfico da função", highlight_points=None, inequacao=None):
    plt.figure(figsize=(5,4))
    plt.plot(x_vals, y_vals, label='f(x)', color='blue')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    if highlight_points:
        for x, y, label in highlight_points:
            plt.scatter(x, y, color='red')
            plt.text(x, y, label)
    if inequacao:
        x_min, x_max = inequacao
        plt.fill_between(x_vals, y_vals.min()-1, y_vals.max()+1, 
                         where=(x_vals>=x_min) & (x_vals<=x_max), 
                         color='green', alpha=0.3, label='Inequação verdadeira')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_base64

@app.route('/')
def index():
    return render_template('index.html', resultado='')

@app.route('/calcular', methods=['POST'])
def calcular():
    form = request.form
    escolha = form.get('escolha', '')
    r = ''

    if escolha == 'funcaoquadratica':
        a = try_float(form.get('a'))
        b = try_float(form.get('b'))
        c = try_float(form.get('c'))
        x_input = try_float(form.get('x'))

        if None in (a, b, c):
            r = 'Informe A, B e C corretamente.'
        else:
            r += f'Função: f(x) = {format_number(a)}x² + {format_number(b)}x + {format_number(c)}<br></br>'
            concavidade = "concavidade para cima" if a>0 else "concavidade para baixo" if a<0 else "não é função quadrática (a=0)"
            r += f'Concavidade: {concavidade}<br></br>'

            xv = -b/(2*a)
            yv = a*xv**2 + b*xv + c
            r += f'Vertice: Xv={format_number(xv)}, Yv={format_number(yv)}<br></br>'

            delta = b*b - 4*a*c
            r += f'Δ = {format_number(delta)}<br></br>'
            if delta < 0:
                r += 'Não existem raízes reais.<br></br>'
            elif delta == 0:
                raiz = -b/(2*a)
                r += f'Raiz única: x = {format_number(raiz)}<br></br>'
            else:
                r1 = (-b + math.sqrt(delta))/(2*a)
                r2 = (-b - math.sqrt(delta))/(2*a)
                r += f'Raízes: x₁ = {format_number(r1)} , x₂ = {format_number(r2)}<br></br>'

            if x_input is not None:
                fx = a*x_input**2 + b*x_input + c
                r += f'F({format_number(x_input)}) = {format_number(fx)}<br>'

            x_vals = np.linspace(xv-10, xv+10, 400)
            y_vals = a*x_vals**2 + b*x_vals + c
            highlight = [(xv, yv, f'Vertice ({format_number(xv)},{format_number(yv)})')]
            if x_input is not None:
                highlight.append((x_input, fx, f'F({format_number(x_input)})={format_number(fx)}'))
            img_base64 = plot_func(x_vals, y_vals, title="Função Quadrática", highlight_points=highlight)
            r += f'<br><img src="data:image/png;base64,{img_base64}"/>'

    elif escolha == 'funcaoafim':
        a = try_float(form.get('a'))
        b = try_float(form.get('b'))
        x_input = try_float(form.get('x'))
        if None in (a, b):
            r = 'Informe A e B corretamente.'
        else:
            r = f'Função afim: f(x) = {format_number(a)}x + {format_number(b)}<br></br>'
            if a > 0:
                r += 'A função é crescente.<br></br>'
            elif a < 0:
                r += 'A função é decrescente.<br></br>'
            else:
                r += 'Função constante.<br></br>'

            if a != 0:
                raiz = -b / a
                r += f'Raiz da função: x = {format_number(raiz)}<br></br>'
            else:
                r += 'Função constante não possui raiz.<br></br>'

            if x_input is not None:
                fx = a*x_input + b
                r += f'F({format_number(x_input)}) = {format_number(fx)}<br>'

            x_vals = np.linspace(-10, 10, 400)
            y_vals = a*x_vals + b
            highlight = []
            if a != 0:
                highlight.append((raiz, 0, f'Raiz ({format_number(raiz)},0)'))
            if x_input is not None:
                highlight.append((x_input, fx, f'F({format_number(x_input)})={format_number(fx)}'))
            img_base64 = plot_func(x_vals, y_vals, title="Função Afim", highlight_points=highlight)
            r += f'<br><img src="data:image/png;base64,{img_base64}"/>'

    elif escolha == 'funcaoexponencial':
        a = try_float(form.get('a'))
        b = try_float(form.get('b'))
        x_input = try_float(form.get('x'))
        if None in (a, b):
            r = 'Informe A e B corretamente.'
        else:
            if x_input is not None:
                fx = a*(b**x_input)
                r += f'F({format_number(x_input)}) = {format_number(fx)}<br>'

            x_vals = np.linspace(-5, 5, 400)
            y_vals = a*(b**x_vals)
            highlight = []
            if x_input is not None:
                highlight.append((x_input, fx, f'F({format_number(x_input)})={format_number(fx)}'))
            img_base64 = plot_func(x_vals, y_vals, title="Função Exponencial", highlight_points=highlight)
            r += f'<br><img src="data:image/png;base64,{img_base64}"/>'

    elif escolha == 'inequacao':
        a = try_float(form.get('a'))
        b = try_float(form.get('b'))
        x_input = try_float(form.get('x')) 
        sinal = form.get('sinal', '').strip()
        c = try_float(form.get('c')) or 0

        if None in (a, b) or sinal == '':
            r = 'Informe A, B e o sinal corretamente.'
        else:
            if a == 0:
                if eval(f"{b} {sinal} {c}"):
                    r = f"Inequação verdadeira para todo x ∈ ℝ<br>"
                else:
                    r = f"Inequação falsa para todo x ∈ ℝ<br>"
            else:
                limite = (c - b) / a
                if a > 0:
                    if sinal == '>':
                        intervalo = f"x > {format_number(limite)}"
                    elif sinal == '>=':
                        intervalo = f"x ≥ {format_number(limite)}"
                    elif sinal == '<':
                        intervalo = f"x < {format_number(limite)}"
                    elif sinal == '<=':
                        intervalo = f"x ≤ {format_number(limite)}"
                else:
                    if sinal == '>':
                        intervalo = f"x < {format_number(limite)}"
                    elif sinal == '>=':
                        intervalo = f"x ≤ {format_number(limite)}"
                    elif sinal == '<':
                        intervalo = f"x > {format_number(limite)}"
                    elif sinal == '<=':
                        intervalo = f"x ≥ {format_number(limite)}"
                r = f"Inequação verdadeira para: {intervalo}<br>"

            if x_input is not None:
                resultado_x = eval(f"{a*x_input + b} {sinal} {c}")
                VF = "Verdadeira" if resultado_x else "Falsa"
                r += f"Para x = {format_number(x_input)}, a inequação é {VF}<br>"

            x_vals = np.linspace(-10, 10, 400)
            y_vals = a*x_vals + b
            inequacao_interval = None
            if a != 0:
                if a>0 and sinal in ['>','>=']:
                    inequacao_interval = (limite, x_vals.max())
                elif a>0 and sinal in ['<','<=']:
                    inequacao_interval = (x_vals.min(), limite)
                elif a<0 and sinal in ['>','>=']:
                    inequacao_interval = (x_vals.min(), limite)
                elif a<0 and sinal in ['<','<=']:
                    inequacao_interval = (limite, x_vals.max())
            highlight = []
            if x_input is not None:
                highlight.append((x_input, a*x_input + b, f'F({format_number(x_input)})={format_number(a*x_input+b)}'))
            img_base64 = plot_func(x_vals, y_vals, title="Inequação Linear", highlight_points=highlight, inequacao=inequacao_interval)
            r += f'<br><img src="data:image/png;base64,{img_base64}"/>'

    elif escolha == 'jurossimples':
        taxa = try_float(form.get('taxa'))
        capital = try_float(form.get('capital'))
        tempo = try_float(form.get('tempo'))
        if None in (taxa, capital, tempo):
            r = 'Informe taxa, capital e tempo corretamente.'
        else:
            juros = capital * (taxa/100) * tempo
            montante = capital + juros
            r = f'Juros = {format_number(juros)} | Montante final = {format_number(montante)}'

    elif escolha == 'juroscompostos':
        taxa = try_float(form.get('taxa'))
        capital = try_float(form.get('capital'))
        tempo = try_float(form.get('tempo'))
        if None in (taxa, capital, tempo):
            r = 'Informe taxa, capital e tempo corretamente.'
        else:
            montante = capital * ((1 + taxa/100) ** tempo)
            juros = montante - capital
            r = f'Juros = {format_number(juros)} | Montante final = {format_number(montante)}'

    elif escolha == 'areaquadrado':
        lado = try_float(form.get('lado'))
        r = f'Área do quadrado = {format_number(lado*lado)}' if lado is not None else 'Informe o lado corretamente.'
    elif escolha == 'arearetangulo':
        base = try_float(form.get('base'))
        altura = try_float(form.get('altura'))
        r = f'Área do retângulo = {format_number(base*altura)}' if None not in (base, altura) else 'Informe base e altura corretamente.'
    elif escolha == 'areatriangulo':
        base = try_float(form.get('base'))
        altura = try_float(form.get('altura'))
        r = f'Área do triângulo = {format_number(base*altura/2)}' if None not in (base, altura) else 'Informe base e altura corretamente.'
    elif escolha == 'areacirculo':
        raio = try_float(form.get('raio'))
        r = f'Área do círculo = {format_number(math.pi * raio * raio)}' if raio is not None else 'Informe o raio corretamente.'
    elif escolha == 'volumecubo':
        lado = try_float(form.get('lado'))
        r = f'Volume do cubo = {format_number(lado**3)}' if lado is not None else 'Informe o lado corretamente.'
    elif escolha == 'volumecilindro':
        raio = try_float(form.get('raio'))
        altura = try_float(form.get('altura'))
        r = f'Volume do cilindro = {format_number(math.pi * raio**2 * altura)}' if None not in (raio, altura) else 'Informe raio e altura corretamente.'
    elif escolha == 'volumeprisma':
        area = try_float(form.get('area')) or try_float(form.get('Área'))
        altura = try_float(form.get('altura'))
        r = f'Volume do prisma = {format_number(area * altura)}' if None not in (area, altura) else 'Informe área da base e altura corretamente.'
    elif escolha == 'volumeesfera':
        raio = try_float(form.get('raio'))
        r = f'Volume da esfera = {format_number(4/3 * math.pi * raio**3)}' if raio is not None else 'Informe o raio corretamente.'

    else:
        r = 'Operação inválida ou não selecionada.'

    return render_template('index.html', resultado=r)

if __name__ == '__main__':
    app.run(debug=True)
