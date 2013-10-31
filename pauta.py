# -*- coding: utf-8 -*-
from lxml.etree import parse
from random import shuffle
import re, os, json
from helper import *

def getPL(cod):
    url = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp='+cod
    soup = parse(urlopen(url))
    if (soup.xpath('//Situacao')[0].text) != '':
        return 'O ' + soup.xpath('//nomeProposicao')[0].text + ' foi para a ' + soup.xpath('//Situacao')[0].text + '\n'

def getPauta(data, orgao='180'):
    url = 'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterPauta?IDOrgao='+orgao+'&datIni='+data+'&datFim=' + data
    soup = parse(urlopen(url))
    reunioes = []
    for index, reuniao in enumerate(soup.xpath('//reuniao')):
        r = {}
        r['id'] = reuniao.xpath('./codReuniao')[0].text
        r['horario'] = reuniao.xpath('./horario')[0].text
        r['estado'] = reuniao.xpath('./estado')[0].text
        r['tipo'] = reuniao.xpath('./tipo')[0].text
        r['proposicoes'] = []
        for proposicao in reuniao.xpath('./proposicoes/proposicao'):
            pl = re.search('([A-Z]*) ([0-9]*)/([0-9]{4})', proposicao.xpath('./sigla')[0].text).groups()
            p = {} #arrumar
            p['tipo'] = pl[0]
            p['numero'] = pl[1]
            p['ano'] = pl[2]
            p['ementa'] = proposicao.xpath('./ementa')[0].text
            if p['tipo'] == 'PL':
                p['quorum'] = 'Maioria Simples'
                p['quorum_num'] = None
            if p['tipo'] == 'PLC':
                p['quorum'] = 'Maioria Absoluta'
                p['quorum_num'] = 257
            if p['tipo'] == 'PEC':
                p['quorum'] = '3/5'
                p['quorum_num'] = 308
            p['votacoes'] = getVotacao(data, pl)
            r['proposicoes'].append(p)
        r['objeto'] = reuniao.xpath('./objeto')[0].text
        reunioes.append(r)
    return reunioes

def getVotacao(data, pl):
    url = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo='+pl[0]+'&numero='+pl[1]+'&ano='+pl[2]
    try:
        soup = parse(urlopen(url))
        votacoes = []
        for votacao in soup.xpath('//Votacao[@Data="'+data+'"]'):
            v = {}
            v['resumo'] = votacao.get('Resumo').strip()
            v['objeto'] = votacao.get('ObjVotacao').strip()
            v['hora'] = votacao.get('Hora').strip()
            v['orientacao'] = []
            for b in votacao.xpath('./orientacaoBancada/bancada'):
                bancada = {
                    'sigla' : b.get('Sigla').strip(),
                    'orientacao': b.get('orientacao').strip()
                }
                v['orientacao'].append(bancada)
            v['votos'] = {
                'sim' : 0,
                'nao' : 0,
                'abstencao' : 0
            }
            for dep in votacao.xpath('./votos/Deputados'):
                if dep.get('Voto') == 'Sim':
                    v['votos']['sim'] += 1
                elif dep.get('Voto') == u'Não':
                    v['votos']['nao'] += 1
                elif dep.get('Voto') == u'Abstenção':
                    v['votos']['abstencao'] += 1
            votacoes.append(v)
        return votacoes
    except urllib2.HTTPError, err:
        votacoes = getRedacaoFinal(pl) # Testa se tem redacao final
        return votacoes

def getRedacaoFinal(pl):
    url = 'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterEmendasSubstitutivoRedacaoFinal?tipo='+pl[0]+'&numero='+pl[1]+'&ano='+pl[2]
    soup = parse(urlopen(url))
    if soup.xpath('//RedacaoFinal'):
        return [{'resumo' : 'Aprovada'}]
    else:
        return [{'resumo' : 'Dificil dizer...'}]

def getPresenca(data):
    url = 'http://www.camara.gov.br/SitCamaraWS/sessoesreunioes.asmx/ListarPresencasDia?data='+data+'&numLegislatura=54&numMatriculaParlamentar=&siglaPartido=&siglaUF='
    soup = parse(urlopen(url))
    presencas = {}
    for p in soup.xpath('//parlamentar'):
        for sessao in p.xpath('./sessoesDia/sessaoDia'):
            descricao = sessao.xpath('./descricao')[0].text
            if not presencas.has_key(sessao.xpath('./descricao')[0].text):
                presencas[sessao.xpath('./descricao')[0].text] = {
                    'descricao' : descricao,
                    'inicio' : sessao.xpath('./inicio')[0].text,
                    'presenca' : 0,
                    'ausencia' : 0
                }
            if sessao.xpath('./frequencia')[0].text == u'Ausência':
                 presencas[sessao.xpath('./descricao')[0].text]['ausencia'] += 1
            if sessao.xpath('./frequencia')[0].text == u'Presença':
                presencas[sessao.xpath('./descricao')[0].text]['presenca'] += 1
    return presencas

def matchmaker(pautas, presencas_dict):
    presencas = []
    for i in presencas_dict:
        presencas.append(presencas_dict[i])
    index_l  = 0
    for index, data in enumerate(pautas):
        if data['tipo'] == u'Sessão Deliberativa' and data['estado'].strip() != 'Cancelada':
            pautas[index]['extra'] = presencas[index_l]
            index_l += 1
    return pautas

def get_or_save(data):
    arquivo = 'data/'+data.replace('/','-')+'.json'
    if os.path.isfile(arquivo):
        with open(arquivo, 'r') as jason:
            dados = json.loads(jason.read())
    else:
        pauta = getPauta(data)
        presenca = getPresenca(data)
        dados = matchmaker(pauta, presenca)    
        with open(arquivo, 'w') as jason:
            jason.write(json.dumps(dados, indent=4))
    return dados
            
def rockandroll(dia):
    return get_or_save(dia)

#pauta = getPauta('29/10/2013')
#presenca = getPresenca('29/10/2013')
#dados = matchmaker(pauta, presenca)