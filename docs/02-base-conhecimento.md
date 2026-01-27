# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores e evitar respostas repetidas ou inconsistentes |
| `perfil_investidor.json` | JSON | Personalizar orientações financeiras de acordo com o perfil e objetivos do cliente |
| `produtos_financeiros.json` | JSON | Apresentar e explicar produtos financeiros compatíveis com o perfil do cliente |
| `transacoes.csv` | CSV | Analisar padrões de gastos, entradas e saídas para apoio educativo e diagnóstico financeiro |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

## Adaptações nos Dados

Os dados mockados disponibilizados na pasta `data/` foram utilizados como base principal do agente, sem necessidade de alterações estruturais significativas, pois já atendem bem ao objetivo do projeto.

Foram realizadas apenas adaptações conceituais, definindo regras claras de uso dos dados pelo agente:

- O `historico_atendimento.csv` é utilizado exclusivamente para contextualizar interações anteriores, evitando respostas repetidas e garantindo continuidade no atendimento.
- O `perfil_investidor.json` é usado como fonte única de informações sobre perfil, objetivos e tolerância a risco, sem que o agente altere ou infira dados não presentes no arquivo.
- O arquivo `produtos_financeiros.json` contém produtos financeiros fictícios, utilizados apenas para fins educacionais e de simulação, sem representar ofertas reais.
- O `transacoes.csv` é utilizado para análise de padrão de gastos e comportamento financeiro, permitindo diagnósticos básicos e orientações educativas, sem recomendações de investimento automáticas.

Essas adaptações garantem maior controle, transparência e redução de alucinações, alinhando o agente às boas práticas de segurança em aplicações de IA.


---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV e JSON da pasta `data` são carregados no início da sessão do agente.  
Esses dados são processados e inseridos de forma estruturada no contexto do prompt, servindo como **fonte única de conhecimento** para as respostas.

O agente consulta essas informações a cada interação, sem persistência de memória fora da sessão, garantindo que todas as respostas sejam baseadas exclusivamente nos dados fornecidos e evitando alucinações

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados **não são inseridos integralmente no system prompt**.  
Eles são consultados de forma dinâmica conforme a intenção da pergunta do usuário.

O system prompt define o comportamento do agente (GUI), suas regras de segurança e limitações.  
Já os dados relevantes (perfil do cliente, transações, produtos ou histórico) são selecionados e injetados no prompt **apenas quando necessários**, como contexto adicional para a resposta.

Essa abordagem reduz o risco de alucinações, melhora a performance do modelo e garante que o agente responda somente com base nas informações disponíveis.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Contexto do Cliente:

Perfil do Cliente:
Nome: João Silva
Idade: 32 anos
Profissão: Analista de Sistemas
Renda mensal: R$ 5.000
Perfil de investidor: Moderado
Objetivo principal: Construir reserva de emergência
Reserva atual: R$ 10.000 de R$ 15.000

Metas Financeiras:
Completar reserva de emergência até 06/2026
Entrada de apartamento até 12/2027

Resumo de Transações Recentes:
Aluguel: R$ 1.200
Alimentação: R$ 570
Transporte: R$ 295
Lazer: R$ 55,90
Saúde: R$ 188

Produtos Financeiros Disponíveis (compatíveis com o perfil):
Tesouro Selic (baixo risco, liquidez diária)
CDB Liquidez Diária (baixo risco)
Fundo Multimercado (risco médio)

Instrução ao Agente:
Responda apenas com base nos dados acima.
Caso a informação solicitada não esteja presente, informe a limitação ao usuário.
...
```
