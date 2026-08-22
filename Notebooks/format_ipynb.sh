for file in *.ipynb; do
    tmp="${file}.tmp"
    jq --sort-keys --indent 1 \
       'walk(if type == "object" and .trusted == false then .trusted = true else . end)' \
       "$file" > "$tmp" && mv "$tmp" "$file"
done
