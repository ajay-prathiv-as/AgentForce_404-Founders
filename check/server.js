const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// Serve frontend files from public folder
app.use(express.static(path.join(__dirname, 'public')));

// Example API endpoint
app.post('/beautify', (req, res) => {
  res.json({ beautifiedCode: 'Example beautified code' });
});

// Catch-all route
app.get('/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
