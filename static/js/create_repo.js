document.getElementById('createRepoForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const repoName = document.getElementById('repoName').value;
  const repoDescription = document.getElementById('repoDescription').value;
  
  try {
    const response = await fetch('/create_repo', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ name: repoName, description: repoDescription })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      window.location.href = '/';
    } else {
      document.getElementById('message').textContent = data.message;
    }
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('message').textContent = '创建仓库失败';
  }
});