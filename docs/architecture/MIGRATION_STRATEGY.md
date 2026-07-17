# Estratégia de migração

## Piloto para MVP

1. congelar schema do ledger do piloto;
2. exportar dados sanitizados com versão;
3. validar IDs, relações e hashes;
4. importar em staging PostgreSQL;
5. reconciliar contagens e saldos de XP;
6. executar testes de retenção e permissões;
7. obter aprovação humana;
8. importar produção;
9. manter backup do ledger até aceite final.

## Regras de migration

- migrations são incrementais e versionadas;
- toda migration destrutiva possui backup e plano de rollback;
- `down` pode ser substituído por restauração quando reversão lógica for insegura;
- dados acadêmicos não são descartados silenciosamente;
- IDs estáveis são preservados;
- conteúdo versionado permanece referenciável;
- migration executada não é reescrita; correção usa nova migration.
