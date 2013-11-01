# Resposta no Form de Inscrição

## Integrantes
Pedro Markun;
Lívia Ascava;
Capi Etheriel;
Todos os servidores da TI da Câmara que ajudaram disponibilizar as bases de dados; 
O Paulo Pimenta e o porteiro da Câmara que me falaram sobre os diferentes tipos de presença;
O servidor que me explicou sobre os quóruns regimentais e deu a sugestão de nome para o projeto;
Todos os Hackers e Beta Testers que leram as tirinhas de papel e ajudaram a encontrar inconsistências; 

## Como foi o processo de produção do projeto durante o Hackathon? 
Tanta gente participou do processo de criação e aperfeiçoamento desse projeto que não faz muito sentido falar em equipe.
Eu me inscrevi sozinho justamente para ter a liberdade de flanar por outros projetos, outras equipes e outras ideias.

A ideia de usar impressora térmica para imprimir bits de informação legislativa não é nova - surgiu em algum momento do ano passado - e é um dos entregaveis que a equipe do Monitor Legislativo vai ter que fazer para um outro projeto - unindo o útil ao útil.

Isso posto, o código inicial do arduino foi desenvolvido faz duas semanas no hackathon do governo de minas - fiz uma primeira versão que imprima dados do orçamento.

Nesse Hackathon depois de aperfeiçoar significativamente o código da impressora e dos controles (obrigado Luis Leão, pelos ensinamentos sobre pull-up resistor) comecei a garimpar e mapear os dados disponíveis que poderiam dar um bom extrato.

Existe uma grande quantidade de dados disponíveis e boa parte do problema foi criar um recorte que fizesse sentido.

A pauta de Plenário (que não esta mapeada no XML da lista de orgãos e foi descoberta em uma conversa com um servidor da casa - novamente obrigado Luis Leão!) acabou sendo um excelente ponto de partida.

Ainda assim, deu bastante trabalho. As bases de dados não são facilmente cruzaveis e até poucas horas atrás estava com um resultado diferente de presença nas bases consultadas - depois de muito penar do Carlos Augusto e sua trupe - acabamos confirmando que o erro era meu - numa tentativa de parear as bases de presença e votação que obviamente deu errado.

Inferir os quóruns mínimos de presença e votação também deu algum trabalho e gerou boas conversas - com direito a descobrir que em alguns momentos não temos 513 deputados - mas que isso não altera a maioria absoluta - mesmo que isso não faça sentido matemático.

Por fim, vários problemas ficaram pendentes... uma das ideias iniciais era mapear as palavras chaves do dia nos discursos - esses dados estão disponíveis em tempo real na página mais demoram tempo demais para aparecer na base aberta. E mesmo assim aparecem consolidados em uma versão de RTF encodado em base64. Meio trevas.

A outra coisa que ficou pendente foi uma forma fácil e estruturada de saber se um projeto já foi votado ou não.
Não existe na base da Câmara uma maneira objetiva de saber isso - usei algumas técnicas (checar votação nominal, checar se o projeto tem redação final) mas elas continuam não servindo para todos os casos e eu não tenho como afirmar, por exemplo, se um REQ (requerimento) foi ou não aprovado a não ser que eu leia a descrição do campo de tramitação.
[É possível fazer o computador inferir a partir desse campo, mas é um pouco contra a lógica de dados estruturados e não da pra ter segurança total no resultado.]