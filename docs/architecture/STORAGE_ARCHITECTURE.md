# Arquitetura de armazenamento

| Informação | Armazenamento | Política |
|---|---|---|
| conteúdo, decisões e código | GitHub | público e versionado |
| progresso, notas e XP | banco privado | acesso por usuário e papel |
| arquivos de evidência | object storage privado | criptografia e URLs temporárias |
| segredos | secret manager | nunca no Git ou banco acadêmico |
| auditoria | banco append-only | retenção e exportação |
| cache | armazenamento efêmero | nunca fonte de verdade |

## Piloto

- `pilot_academic.sqlite3` fora do Git;
- backup privado criptografado;
- anexos em diretório privado com hash e metadados;
- exportação JSON sanitizada para migração e auditoria.

## MVP

PostgreSQL com migrations versionadas, object storage compatível com S3, backups testados e política de restauração. Separar bucket público de recursos educacionais e bucket privado de evidências.
