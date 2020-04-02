#!/usr/bin/env bash

for tool_dir in $(ls tools); do

  SLUG_TOOL_NAME=$(echo ${tool_dir} | sed 's/_/-/')
  DOC_PATH_PLUGIN=docs/content/docs/${SLUG_TOOL_NAME}
  README_PATH="tools/${tool_dir}/README.md"

  mkdir -p "${DOC_PATH_PLUGIN}"

  # Get plugin title
  TITLE=$(head -n 1 ${README_PATH} | sed 's/^#//' | sed 's/^[ \t]*//')
  echo "---\ntitle: ${TITLE}\n---\n" > "${DOC_PATH_PLUGIN}/index.md"
  cat "tools/${tool_dir}/README.md" >> "${DOC_PATH_PLUGIN}/index.md"

done