for file in *.ipynb; do jq --indent 1 . "$file" > tmp && mv tmp "$file"; done
