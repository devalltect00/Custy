npm install -g @mermaid-js/mermaid-cli

To create the image
mmdc -i DIAGRAMS.md -o diagrams.png


Steps:

``` (recommended using git bash)
# Step 1
py tools/generate_diagram/generate_diagram_mmd.py

# Step 2
bash tools/generate_diagram/export_diagrams.sh
```
