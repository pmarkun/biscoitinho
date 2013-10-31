# Extrato Legislativo

Esse projeto foi desenvolvido durante o Hackathon na Câmara - entre 29/10/2010 e 01/11/2010.

## Funcionamento

O Extrato Legislativo é um conjunto de tecnologias e scripts que alimentam uma impressora térmica (essas de notas fiscais) com
informações políticas - um retrato das atividades do plenário em um determinado dia.

A ideia por traz da instalação é materializar a informação política que normalmente fica disponível apenas na rede, alienada do dia a dia das pessoas.

O sistema é divido em duas partes:

### Impressora Térmica e Arduino
Usamos uma impressora termica conectada a um Arduino (um hardware aberto para prototipação rápida) com um Shield Ethernet (que permite que o Arduino e a Impressora se liguem na internet) para imprimir os extratos.

O sistema roda com 5-9v e aproximadamente ~2a - e esta pronto para funcionar com bateria. É também possível utiliza-lo com um Shield WiFi permitindo que ele acesse o servidor sem usar fios.

### Servidor
Usamos o framework de Python chamado Flask para gerar uma pequeno serviço web que consome os dados do Portal de Dados Abertos da Câmara e transforma em bits de informação para a impressora térmica. Leia o arquivo requirements.txt.

Toda vez que o serviço é acessado ele busca as informações em tempo real disponíveis na Câmara - infelizmente parte das informações
disponíveis em formato aberto são disponibilizadas apenas no fim do dia (ou alguns dias depois - como é o caso dos discursos) tornado
o aplicativo um pouco menos interessante e incapaz de responder rapidamente aos acontecimentos da casa.

Atualmente os dados utilizados pelo aplicativo incluem:
  * Pauta do Plenario
  * Votação em Plenario
  * Orientação das Bancadas
  * Matérias Legislativa com Redação Final
  * Presença em Plenario
  * Quórum Regimental

Outros dados e serviços podem ser acoplados com facilidade ao sistema - ampliando e customizando as possibilidades de impressão do extrato legislativo.

O sistema conta também com um Simulador que permite ter uma ideia de como vai ficar a impressão, facilitando a prototipagem.

### Implementações Possíveis e Futuro

A ideia é que esse protótipo se desenvolva e ganhe corpo. Assim que tivermos uma versão mais acabada e com uma caixa única ela podera ser colocada em diferentes locais com circulação pública como a própria Câmara, equipamentos públicos, bares e organizações sociais.

Cada kit de impressora e componentes deve custar em torno de r$150 - pensando ai em uma escala artesanal de produção.

O preço das bobinas de papel é trivial, cerca de r$1,20 por bobina de 30 metros. A titulo de curiosidade o extrato do dia 29/10 (uma terça-feira) mede 54,13cm (menos de r$0.02 por impressão) o extrato de sexta-feira tem em média 15cm.