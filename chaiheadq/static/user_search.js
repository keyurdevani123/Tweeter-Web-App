const searchInput = document.getElementById('search-input');
const userList = document.getElementById('user-list');

searchInput.addEventListener('input', function() {
    const query = searchInput.value;

    if (query.length >= 1) {
        // Make an AJAX request to get users
        fetch("/user_search/?query=" + query)
            .then(response => response.json())
            .then(data => {
                userList.innerHTML = '';  // Clear previous results
                if (data.results.length > 0) {
                    data.results.forEach(user => {
                        const div = document.createElement('div');
                        div.classList.add('user-list-item');
                        div.innerHTML = `
                            <img src="${user.profile_image}" alt="${user.username}" class="rounded-circle" style="width: 30px; height: 30px; margin-right: 10px;">
                            <span style="font-size: 14px; color: #333;">${user.username}</span>
                        `;
                        div.onclick = () => window.location.href = `/user/details/${user.user_id}/`;  // Redirect to user details page
                        userList.appendChild(div);
                    });
                    userList.style.display = 'block';  // Show the user list
                } else {
                    userList.style.display = 'none';  // Hide if no results
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        userList.style.display = 'none';  // Hide the user list if the search is empty
    }
});
