# Modelo de auditoria

## Eventos auditáveis

- autenticação e alteração de papel;
- criação, publicação e depreciação de conteúdo;
- início, envio e avaliação de tentativa;
- upload, acesso e exclusão de evidência;
- concessão ou reversão de XP;
- execução e validação de prompt ou Skill;
- alterações de política;
- sincronização com GitHub e Linear;
- ações administrativas e integrações externas.

## Campos mínimos

```text
audit_id
occurred_at
actor_type
actor_id
action
resource_type
resource_id
correlation_id
source_surface
sensitivity
result
reason_code
before_hash
after_hash
metadata_sanitized
```

Logs não armazenam conteúdo sensível desnecessário, prompts completos privados, tokens ou credenciais. Retificações usam evento compensatório, não edição silenciosa.
