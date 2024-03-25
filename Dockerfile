FROM codercom/code-server:latest
COPY index.js .
CMD ["node", "index.js"]
