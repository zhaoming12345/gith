document.addEventListener('DOMContentLoaded', function() {
    fetchRepositories();
});

function fetchRepositories() {
    fetch('/get_repositories')
        .then(response => response.json())
        .then(data => {
            if (data.repositories) {
                displayRepositories(data.repositories);
            } else {
                showMessage('获取仓库列表失败', true);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('获取仓库列表失败', true);
        });
}

function displayRepositories(repositories) {
    const repoList = document.getElementById('repoList');
    repoList.innerHTML = '';

    if (repositories.length === 0) {
        repoList.innerHTML = '<p class="no-repos">暂无仓库</p>';
        return;
    }

    repositories.forEach(repo => {
        const repoElement = document.createElement('div');
        repoElement.className = 'repo-item';
        repoElement.innerHTML = `
            <h3>${repo.name}</h3>
            <p>${repo.description || '暂无描述'}</p>
            <p class="creator">创建者: ${repo.creator_username}</p>
        `;
        repoList.appendChild(repoElement);
    });
}

function showMessage(message, isError = false) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message;
    messageElement.className = isError ? 'error' : 'success';
    messageElement.style.display = 'block';

    setTimeout(() => {
        messageElement.style.display = 'none';
    }, 3000);
}