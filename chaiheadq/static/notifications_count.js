document.addEventListener("DOMContentLoaded", () => {
    const unreadCount = document.getElementById("unread-count");

    const fetchUnreadCount = () => {
        fetch("/notifications/get/")
            .then(response => response.json())
            .then(data => {
                const count = data.notifications_count || 0;
                unreadCount.style.display = count > 0 ? "inline" : "none";
                unreadCount.textContent = count;
            })
            .catch(console.error);
    };

    fetchUnreadCount();
    setInterval(fetchUnreadCount, 120000); // Refresh every 2 minutes
    //notificationLink.addEventListener("click", markAllAsRead);
});
