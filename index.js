const http = require('http');
const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  const password = process.env.PASSWORD;
  console.log(`Password: ${password}`);

  if (!password) {
    console.log('PASSWORD environment variable not set');
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/plain');
    res.end('PASSWORD environment variable not set');
    return;
  }

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`Code-Server Password: ${password}`);
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
