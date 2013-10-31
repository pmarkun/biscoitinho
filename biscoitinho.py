# -*- coding: utf-8 -*-
from flask import Flask, render_template
from unidecode import unidecode
from datetime import datetime

app = Flask(__name__)

START = chr(3) # Caracter ASCII que inicia o conteudo
END = '\n\n'

def thermalprint(data, template='pauta.html', ext='base_raw.html'):  
    return unidecode(render_template(template, ext=ext, data=data, START=START, END=END, lstrip_blocks=True, trim_blocks=True))

#@app.route('/')
#@app.route('/<fake>')
def sample(fake=False):
    texto = ''
    texto += '========== HACKATHON =========\n'
    texto += '       EXTRATO POLITICO       \n'
    texto += '======== DADOS SAMPLE ========\n'
   
    texto += 'Hello Printer!'
    if fake:
        return simulate(texto)
    return thermalprint(texto)

import pauta
@app.route('/')
@app.route('/<tempo>')
@app.route('/<tempo>/<fake>')
def hubbahubba(tempo=None, fake=False):
    if tempo:
        dia = tempo.replace('-','/')
    else:
        tempo = datetime.now() 
        dia = '/'.join([str(tempo.day),str(tempo.month),str(tempo.year)])
        
    ##DIA MANUAL
    dia = '25/10/2013'

    data = {
        'pautas' : pauta.rockandroll(dia),
        'local' : 'CAMARA FEDERAL',
        'dia'   : dia,
        'hora'  : '10:19'
        }
    data['pautas'].reverse()
    if fake:
        return thermalprint(data, 'pauta.html', 'base_fake.html')
    return thermalprint(data, 'pauta.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')