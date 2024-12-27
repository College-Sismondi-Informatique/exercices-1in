for file in *.ipynb; do jq --sort-keys  --indent 1 . "$file" > tmp && mv tmp "$file"; done
