# Evidências estáticas — FMRTE v1.0.0.5

Fonte: ZIP fornecido pelo proprietário do projeto; inspeção offline de PE/CLI, metadados #Strings, configuração XML e recursos. O EXE **não foi executado**.

## Binário analisado
- `FMRTE.exe`, 649728 bytes, SHA-256: `e7ba25394eb1f69fc73814a4cbe198a45a5681670f7472a07d9ba9f2a0b3fb07`.
- PE32, Intel x86 (machine 0x14c), GUI Windows, CLR com metadados `v2.0.50727`, flags ILONLY e 32BITREQUIRED.
- Metadados referenciam `System.Windows.Forms`; arquitetura original parece WinForms, não WPF.
- `config.xml`: LangFile=english.xml; Currency=Pound; Debug=False; AttributesRangeMultiplier=5.
- Idiomas: 546 chaves em english.xml e 544 em portugues.xml; português parcialmente traduzido.

## Indicadores internos relevantes
- Memória: `ProcessMemoryReader`, `ReadProcessMemory`, `WriteProcessMemory`, `VirtualQueryEx`, `MemoryFreeze`, `RegularMemoryScan`, `IrregularMemoryScan`.
- Versões: `v8_0_0`, `v8_0_1`, `v8_0_2v1`, `v8_0_2v2` e métodos `loadOffsets_8_0_*`.
- Domínio: `Player`, `Person`, `Club`, `Nation`, `League`, `Contract`, `LoanContract`, `Stadium`, `Relations`.
- Interface: `cloneCenter`, `clubsAffiliations`, `leagueStandings`, `playersPositions`, `playersPrefMoves`.
- Busca e edição: `searchPlayersByID`, `searchPlayersByName`, `savePlayer`, `saveContract`, `saveFinances`, `saveStadium`.

**Cuidado:** símbolos e rótulos indicam arquitetura e intenções; não comprovam funcionamento, suporte efetivo de versões ou valores de offsets. Não foram identificados endereços reais. O SHA-256 citado é do *editor*, não do executável *Football Manager 2008*.

## Mudanças propostas para o projeto de mapeamento

1. Criar catálogo por build do jogo com fingerprint SHA-256, arquitetura, patch e proveniência.
2. Tratar as quatro variantes 8.0.0/8.0.1/8.0.2v1/8.0.2v2 apenas como **candidatas de pesquisa**, até obter executáveis do jogo e validar compatibilidade.
3. Decompor estruturas por entidade: Person, Player, Staff, Club, Nation, League, Stadium, Contract, LoanContract e Relations.
4. Evoluir o JSON Schema para tipos e endereçamento nativos comprovados, com campos `sourceEvidence` e estado de validação.
5. Manter a localização e a enumeração de rótulos de UI em arquivos próprios.
6. Preservar exemplos fictícios separados de mapas operacionais.

## Próximo experimento
Identificar uma build **real do jogo**, registrar SHA-256 do executável, testar leitura de uma entidade sem escrita, documentar evidências reproduzíveis.
