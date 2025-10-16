// Simple PDF generation using a different approach
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // For now, return a simple response to test if the endpoint works
  res.status(200).json({ 
    message: "PDF endpoint is working", 
    timestamp: new Date().toISOString() 
  });
}
