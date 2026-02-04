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
Os dados foram utilizados sem alterações estruturais, apenas com regras claras de uso:
- [ ] Produtos são fictícios e usados apenas para fins educacionais;
- [ ] Transações são usadas para diagnóstico básico, não decisões automáticas;
- [ ] O agente não altera nem infere dados inexistentes.
- [ ] Isso reduz risco de alucinação e mantém rastreabilidade.


---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV e JSON são carregados no início da aplicação via Python e utilizados como fonte única de conhecimento durante a sessão.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

- [ ] O system prompt define regras e comportamento;
- [ ] Os dados são consultados dinamicamente conforme a pergunta;
- [ ] Apenas informações relevantes entram no contexto da resposta.

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
