#!/usr/bin/env bash

DOC_BASE=docs/content/docs/
CATALOG_FILE="docs/static/catalog.json"

echo "[\n" > ${CATALOG_FILE}

for tool_dir in $(ls tools); do

  SLUG_TOOL_NAME=$(echo ${tool_dir} | sed 's/_/-/')
  DOC_PATH_PLUGIN="${DOC_BASE}${SLUG_TOOL_NAME}"
  README_PATH="tools/${tool_dir}/README.md"

  mkdir -p "${DOC_PATH_PLUGIN}"

  # Add plugin title to documentation file
  TITLE=$(head -n 1 ${README_PATH} | sed 's/^#//' | sed 's/^[ \t]*//')
  echo "---\ntitle: ${TITLE}\n---\n" > "${DOC_PATH_PLUGIN}/index.md"
  cat "tools/${tool_dir}/README.md" >> "${DOC_PATH_PLUGIN}/index.md"

  # Add metainformation for catalog
  cat "tools/${tool_dir}/META" >> ${CATALOG_FILE}

done

echo "]" >> ${CATALOG_FILE}
