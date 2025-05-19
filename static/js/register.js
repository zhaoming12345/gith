document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  
  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      window.location.href = '/login';
    } else {
      document.getElementById('message').textContent = data.message;
    }
  } catch (error) {
    console.error('Error:', error);
  }
});