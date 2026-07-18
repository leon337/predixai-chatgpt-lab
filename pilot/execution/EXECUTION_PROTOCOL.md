# Protocolo de execução do piloto V0.1

## Pré-condições

1. contratos das 10 missões validados pelo CI;
2. revisão independente em SHA exato;
3. zero P1/P2 pendente;
4. `LEA-24` em andamento;
5. ledger SQLite criado somente em armazenamento privado;
6. usuário inicial identificado como `USR-0001`, sem dados sensíveis no repositório.

## Fluxo por missão

1. confirmar versão e hash do contrato;
2. abrir uma tentativa única no ledger;
3. apresentar contexto, objetivos, conceito e analogia;
4. confirmar ambiente, ferramentas permitidas e restrições;
5. executar etapas salváveis;
6. classificar e armazenar evidências em local privado;
7. aplicar rubrica e requisitos eliminatórios;
8. registrar nota, resultado e XP em transações separadas;
9. executar remediação quando a nota for inferior a 80;
10. agendar revisão de 24 horas;
11. ao concluir o módulo, agendar revisão de 7 dias;
12. liberar a missão seguinte somente após o gate definido.

## Regras acadêmicas

- a primeira tentativa não é apagada por uma remediação;
- erros honestos podem gerar `DEBUG XP`;
- resultado inventado, ausência de evidência ou violação de segurança bloqueia domínio;
- domínio exige nota maior ou igual a 80;
- domínio confirmado exige retenção posterior em PASS;
- a missão-chefe só é liberada após remediações obrigatórias anteriores.

## Privacidade

- respostas reais não entram no GitHub;
- prints sensíveis devem ser apagados após validação;
- evidência pública exige sanitização e aprovação explícita;
- conteúdo `PROHIBITED` não pode ser persistido nem ter hash derivado armazenado;
- segredos acidentalmente expostos exigem exclusão e rotação imediata.

## Interrupção segura

A execução é interrompida quando houver:

- divergência entre contrato e versão carregada;
- indisponibilidade da superfície prática;
- permissão insuficiente;
- risco de privacidade ou segurança;
- necessidade de ação irreversível sem aprovação humana;
- falha de sincronização acadêmica.

## Encerramento do piloto

O relatório final deve distinguir:

- qualidade dos contratos;
- desempenho acadêmico do aluno;
- defeitos das ferramentas;
- limitações do dispositivo ou plano;
- remediações ainda abertas;
- decisão `GO`, `GO_WITH_REMEDIATION` ou `NO_GO` para o MVP web.
