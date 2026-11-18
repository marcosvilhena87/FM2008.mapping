# Metodologia de pesquisa e validação

**Não há offsets ou ponteiros reais confirmados neste repositório.**

1. Inventariar edições/patches, idioma, plataforma, hash SHA-256 e arquitetura do executável.
2. Construir ambiente de testes isolado com cópias dos saves e sem processos críticos.
3. Identificar dados **somente em leitura** e registrar evidências reproduzíveis.
4. Distinguir offsets de arquivo, offsets de estrutura e endereços virtuais de processo.
5. Repetir observações após reiniciar o jogo e carregar diferentes saves.
6. Documentar tamanho, sinal, alinhamento, endianidade, encoding, referências e limites de cada campo.
7. Exigir duas validações independentes por build antes de considerar um mapa confiável.
8. Testar invariantes, rollback e corrupções possíveis antes de habilitar qualquer escrita.

## Registro mínimo de evidência
Para cada campo: build/hash, cenário, tipo, offset, interpretação, repetibilidade, observador, data e limitações. Nunca publicar save pessoal ou dumps com dados sensíveis.

## Não objetivos na fase inicial
Cheats automatizados, bypass de proteção, injeção de código, escrita em builds desconhecidas.
