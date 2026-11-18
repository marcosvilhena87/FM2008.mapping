# Contrato entre os repositórios — v1

## Fonte da verdade
`FM2008.mapping` publica manifestos declarativos; `FMRTE2008` consome **somente artefatos aprovados**. A implementação do editor não deve conter offsets fixos.

## Identidade e compatibilidade
- `schemaVersion`: SemVer; suporte inicial somente a `1.0.0`.
- `build.id`: identificador humano da versão.
- `build.architecture`: `x86` para a versão inicial pesquisada.
- `build.executableSha256`: hash do executável, calculado localmente.
- Match de hash **exato**; ausência ou divergência implica bloqueio de leitura/escrita.
- `maps/examples/` nunca são carregados no modo real.

## Tipos
Inteiros explícitos com sinal, sem sinal e larguras definidas; `f32`/`f64` IEEE-754; `bytes` exige `length`. Endianness inicial: little-endian, a confirmar em testes. Offset relativo ao início da estrutura. Endereçamento de estruturas no processo ainda não está definido.

## Regras de segurança
1. **Modo somente leitura** como padrão.
2. Escrita desativada até haver validação da build, snapshot prévio, limites de valor, verificação do endereço, confirmação do usuário e leitura posterior.
3. Não serializar dados pessoais ou dumps completos em logs.
4. Falha de validação implica comportamento seguro (*fail closed*).
5. O editor nunca deve executar mapeamentos obtidos como código.

## Evolução
Mudança incompatível no contrato incrementa versão major; mudança opcional compatível incrementa minor. Editor deve rejeitar majors não reconhecidos.
