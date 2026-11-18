# Testes de mapeamento

## Fase atual
A validação automatizada está em `tools/validate.py` e é executada no GitHub Actions.

## Próximos testes
- Rejeitar manifestos sem hash SHA-256 válido.
- Rejeitar schema major não suportado.
- Verificar campos fora dos limites da estrutura e sobreposição de offsets.
- Validar tipos e comprimentos de campos binários.
- Proibir `maps/examples/` no catálogo de produção.
- Verificar correspondência exata da build.
