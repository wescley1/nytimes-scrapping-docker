#!/bin/bash

# Variáveis de ambiente
SEARCH_PHRASE="${SEARCH_PHRASE:-"liverpool"}"
CATEGORIES="${CATEGORIES:-"Sports"}"
MONTHS="${MONTHS:-10}"
SORTING="${SORTING:-"newest"}"

# Diretório de resultados
RESULTADOS_DIR="${RESULTADOS_DIR:-"./resultados/output"}"

# Cria o diretório de resultados se ele não existir
mkdir -p "$RESULTADOS_DIR"

# Executa o container Docker
docker run \
    -e SEARCH_PHRASE="$SEARCH_PHRASE" \
    -e CATEGORIES="$CATEGORIES" \
    -e MONTHS="$MONTHS" \
    -e SORTING="$SORTING" \
    -v "$(pwd)/$RESULTADOS_DIR:/projeto/resultados" \
    -v "$(pwd)/.env:/projeto/.env" \
    ghcr.io/wescley1/nytimes-scrapping-docker/one4tech:latest