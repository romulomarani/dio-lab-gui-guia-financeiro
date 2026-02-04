# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

Antes dos testes, os participantes foram informados de que se tratava de um cliente fictício, garantindo compreensão correta do contexto.
---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | Se o agente responde corretamente com base nos dados disponíveis | Se o agente responde corretamente com base nos dados disponíveis |
| **Segurança** | Perguntar gastos por categoria e receber o valor correto do transacoes.csv | Se o agente evita inventar informações ou extrapolar dados |
| **Coerência** | Perguntar algo fora do escopo e o agente admitir a limitação | Se a resposta faz sentido para o perfil do cliente |

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- [ ] Respostas claras e fáceis de entender;
- [ ] Boa aderência aos dados fictícios fornecidos;
- [ ] Postura educativa, sem assumir papel de consultor financeiro;
- [ ] Tratamento adequado de perguntas fora do escopo;
- [ ] Coerência entre perfil do cliente, objetivos e sugestões apresentadas.

**O que pode melhorar:**
- [ ] Ampliação da base de dados fictícia para novos cenários;
- [ ] Inclusão de mais exemplos de metas financeiras;
- [ ] Implementação futura de métricas automáticas de uso e performance.

---

## Métricas Avançadas (Opcional)

Embora não implementadas nesta versão, foram consideradas como evolução futura:
- [ ] Tempo médio de resposta do agente;
- [ ] Registro de erros e falhas;
- [ ] Logs de interações para análise de uso;
- [ ] Monitoramento de custo e performance em aplicações com LLMs.

Ferramentas como LangFuse ou LangWatch poderiam ser utilizadas em versões futuras para observabilidade, mas não foram necessárias para o escopo educacional deste projeto.
