for file in *.ipynb; do jq . "$file" > tmp && mv tmp "$file"; done
