# Constantes históricas extraídas do IL de FMRTE.exe v1.0.0.5

**Estado: `legacy-il-observed`. Não são mapeamentos aprovados e não devem ser carregados pelo editor contra um processo real.**

Fonte original: `FMRTE v1.0.0.5.zip`, `FMRTE.exe`, SHA-256 `e7ba25394eb1f69fc73814a4cbe198a45a5681670f7472a07d9ba9f2a0b3fb07` (hash **do editor**, não do jogo).

Os CSVs aqui versionados reúnem as *diferenças de constantes* obtidas em `version_diff_players.csv` e `version_diff_persons.csv` do pacote de pesquisa de engenharia reversa. Não representam as 859 atribuições do conjunto completo. O dataset integral fica no pacote de pesquisa do projeto e pode ser convertido para o formato de importação com `tools/import_legacy_offsets.py`.

## Proveniência
- `players.csv`: carregadores `FMRTE.GameClasses.Players.loadplayersOffsets_8_0_0`, `_8_0_1`, `_8_0_2v2`.
- `persons.csv`: carregadores `FMRTE.GameClasses.Persons.loadOffsets_8_0_0`, `_8_0_1`, `_8_0_2v1`, `_8_0_2v2`.
- São inteiros **assinados**: ex. `OffsetStaffPlayerAttributesAndPositions=-92`.
- `OffsetPlayer` e `OffsetPersonsList` podem ser candidatos a endereços base; sem inspeção dos chamadores, **não** classificar automaticamente um símbolo `Offset*` como endereço absoluto ou deslocamento relativo.
- Estes CSVs não estão sob `maps/` para evitar confusão com manifestos aprovados.
- A variante 8.0.2v1 não consta da tabela de carregadores de jogadores encontrada, portanto não foi inferida.

## Critério para promoção futura
Confirmar executável do **jogo**, SHA-256 e versão, reprodução em saves, semântica de endereçamento e invariantes, com evidências e testes. Não promover automaticamente conteúdo importado de IL.
