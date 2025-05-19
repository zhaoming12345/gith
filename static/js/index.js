document.getElementById('logoutBtn').addEventListener('click', async () => {
  try {
    const response = await fetch('/logout', {
      method: 'POST'
    });
    
    if (response.ok) {
      window.location.href = '/login';
    }
  } catch (error) {
    console.error('Error:', error);
  }
});

document.getElementById('createRepoBtn').addEventListener('click', function() {
    window.location.href = '/create_repo';
});

document.getElementById('viewRepoBtn').addEventListener('click', function() {
    window.location.href = '/view_repo';
});

async function displayUsername() {
  try {
    const response = await fetch('/get_username');
    const data = await response.json();
    
    if (data.username) {
        document.getElementById('usernameDisplay').textContent = data.username;
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

displayUsername();