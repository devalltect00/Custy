#!/bin/bash

INPUT_DIR="docs/changelog/diagrams"
OUTPUT_DIR="docs/changelog/images"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.mmd; do
  filename=$(basename "$file" .mmd)

  echo "Exporting $filename..."

  # mmdc -i "$file" -o "$OUTPUT_DIR/$filename.svg"
  mmdc -i "$file" -o "$OUTPUT_DIR/$filename.png"
done

echo "Done!"
