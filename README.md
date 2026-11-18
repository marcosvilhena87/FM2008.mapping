# FM2008.mapping

Mapas de dados e contratos versionados para o Football Manager 2008.

> Estado: **arquitetura inicial / pesquisa**. Nenhum endereço, offset ou layout de memória foi confirmado.

## Objetivo
Manter definições **declarativas** (JSON) das versões suportadas do FM2008, dos tipos de campo, estruturas e regras de validação. O projeto **não acessa processos** e **não edita memória**.

## Estrutura
- `schemas/`: esquema JSON para validar manifestos.
- `maps/`: mapas por identificação exata de build (exemplos não operacionais).
- `docs/`: metodologia e formato dos contratos.
- `tools/`: validador independente.
- `tests/`: casos de teste e fixtures.
- `.github/workflows/`: validação contínua.

## Contrato com FMRTE2008
1. Editor coleta a impressão digital do executável (SHA-256 e arquitetura).
2. Resolve manifesto com identidade exata e `schemaVersion` compatível.
3. Rejeita versões desconhecidas, ambíguas ou incompletas.
4. Somente depois habilita leitura; escrita depende de verificações adicionais.

Documentação: [contrato](docs/CONTRACT.md) · [pesquisa](docs/RESEARCH.md) · [roadmap](docs/ROADMAP.md).

## Validação
```bash
python tools/validate.py
```

Exemplos em `maps/examples/` são intencionalmente fictícios, **nunca** devem ser usados contra um jogo em execução.
