document.addEventListener("DOMContentLoaded", function () {
    const unreadCount = document.getElementById("unread-count");

    function updateUnreadCount() {
        fetch("/notifications/get/")
            .then((response) => response.json())
            .then((data) => {
                const count = data.unread_count;
                if (count > 0) {
                    unreadCount.style.display = "inline";
                    unreadCount.textContent = count;
                } else {
                    unreadCount.style.display = "none";
                }
            });
    }

    // Fetch the count initially
    updateUnreadCount();

    // Optional: Poll for updates every 30 seconds
    setInterval(updateUnreadCount, 30000);
});
