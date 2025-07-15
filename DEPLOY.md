# Scripts de Deploy - JsonPort

Este documento explica como usar os scripts de deploy para sincronizar o changelog e publicar no PyPI.

## Scripts Disponíveis

### `deploy.sh` (Principal)
Script principal que gerencia todo o processo de deploy.

**Uso:**
```bash
./deploy.sh [--publish] [--version=VERSION]
```

**Argumentos:**
- `--publish`: Publica no PyPI (opcional)
- `--version=VERSION`: Versão específica (opcional, usa versão do pyproject.toml se não especificado)

**Exemplos:**
```bash
# Build apenas (sem publicar)
./deploy.sh

# Build e publicar no PyPI
./deploy.sh --publish

# Build com versão específica
./deploy.sh --version=1.1.0

# Build e publicar com versão específica
./deploy.sh --publish --version=1.1.0
```

### `release.sh` (Auxiliar)
Script interativo que facilita o processo de release.

**Uso:**
```bash
./release.sh
```

Este script:
1. Verifica se há mudanças no core (jsonport/ e tests/)
2. Se houver mudanças, sugere fazer uma nova release
3. Se não houver mudanças, oferece opções interativas

## O que o Script Faz

### 1. Verificações Iniciais
- ✅ Verifica se está no diretório correto
- ✅ Verifica se ~/.pypirc existe
- ✅ Verifica se há mudanças não commitadas
- ✅ Verifica se a versão já existe no PyPI

### 2. Atualização do Changelog
- ✅ Substitui `[Unreleased]` pela versão atual
- ✅ Atualiza links de comparação
- ✅ Adiciona link para a nova versão
- ✅ Cria backup antes de modificar

### 3. Testes e Qualidade
- ✅ Executa todos os testes com pytest
- ✅ Verifica formatação com black
- ✅ Verifica linting com flake8
- ✅ Verifica tipos com mypy

### 4. Build e Publicação
- ✅ Limpa builds anteriores
- ✅ Constrói o pacote (tar.gz e wheel)
- ✅ Publica no PyPI (se --publish for usado)

### 5. Git e GitHub
- ✅ Commit das mudanças no changelog
- ✅ Cria tag da versão
- ✅ Push para GitHub (main + tag)

## Configuração Necessária

### 1. ~/.pypirc
Configure suas credenciais do PyPI:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-TOKEN_AQUI
```

### 2. Dependências
Certifique-se de ter instalado:
```bash
pip install build twine pytest black flake8 mypy
```

## Fluxo de Trabalho Recomendado

### Para Desenvolvimento Diário
```bash
# Apenas build e testes
./deploy.sh
```

### Para Releases
```bash
# Usar o script interativo
./release.sh

# Ou diretamente
./deploy.sh --publish
```

### Para Hotfixes
```bash
# Especificar versão manualmente
./deploy.sh --publish --version=1.0.2
```

## Segurança

- ✅ Scripts não são versionados (estão no .gitignore)
- ✅ Verifica credenciais antes de publicar
- ✅ Cria backup do changelog antes de modificar
- ✅ Restaura backup em caso de erro
- ✅ Verifica se versão já existe no PyPI

## Troubleshooting

### Erro: "~/.pypirc não encontrado"
Configure suas credenciais do PyPI conforme documentado acima.

### Erro: "Versão já existe no PyPI"
Atualize a versão no `pyproject.toml` antes de executar o script.

### Erro: "Testes falharam"
Corrija os testes antes de tentar novamente. O script restaura o changelog automaticamente.

### Erro: "Build falhou"
Verifique se todas as dependências estão instaladas e se o código está correto.

## Notas Importantes

1. **Sempre teste localmente** antes de publicar
2. **Verifique o changelog** antes de fazer commit
3. **Use tags semânticas** (v1.0.0, v1.1.0, etc.)
4. **O script é idempotente** - pode ser executado múltiplas vezes
5. **Backup automático** - o changelog é restaurado em caso de erro 