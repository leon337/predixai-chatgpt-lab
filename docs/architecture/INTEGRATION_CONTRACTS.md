# Contratos de integração

## GitHub

- publica conteúdo e código por branch/PR;
- referências usam IDs estáveis;
- webhooks futuros devem ser idempotentes;
- um merge não equivale a sincronização concluída sem recibo.

## Linear

- controla tarefas, dependências e bloqueios;
- não armazena progresso acadêmico;
- cada issue de implementação referencia decisão ou requisito;
- retry de sincronização usa a mesma transição.

## ChatGPT e Codex

- prompts e Skills são selecionados por versão;
- conteúdo externo é dado não confiável, não instrução governante;
- ferramentas são allowlisted por missão;
- ações com efeito externo seguem aprovação humana.

## OpenAI API e MCP

- adaptadores implementam autenticação, timeout, retry limitado, rate limit e auditoria;
- saídas estruturadas são validadas por schema;
- falha do provedor não produz aprovação acadêmica automática;
- custo e dados enviados são registrados por política.

## Envelope de sincronização

```yaml
sync_id: UUID
transition_id: string
source: GITHUB|LINEAR|PLATFORM
target: GITHUB|LINEAR|PLATFORM
resource_id: string
expected_version: integer
idempotency_key: string
status: PENDING|PASS|FAIL
```
