$projectPath = "C:\Users\James\Desktop\code\RAGENToolbox"

docker run -it --rm `
  -v "${projectPath}:/app" `
  -w /app `
  --name lapp `
  python:3.13.9-slim `
  /bin/bash
