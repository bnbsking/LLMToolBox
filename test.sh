# /bin/bash

projectPath="/home/james/Desktop/code/RAGENToolbox"

docker run -it --rm \
  -v "${projectPath}:/app" \
  -w /app \
  --name lapp \
  3.13.9-slim \
  /bin/bash
