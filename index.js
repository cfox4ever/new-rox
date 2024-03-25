const http = require('http');
const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  const password = process.env.PASSWORD || '62c470975e3a084ba385b22f0a16c0d4';

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`Code-Server Password: ${password}`);
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
