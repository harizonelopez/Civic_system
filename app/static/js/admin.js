document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("adminSidebar");
    const menuToggle = document.getElementById("adminMenuToggle");
    if (!sidebar || !menuToggle) {
        return;
    }

    // Toggle sidebar
    menuToggle.addEventListener("click", function () {
        const isOpen = sidebar.classList.toggle("show");

        menuToggle.setAttribute("aria-expanded", isOpen);
    });

    // Close sidebar after selecting a navigation link
    const navigationLinks = sidebar.querySelectorAll(".admin-nav-link");

    navigationLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            sidebar.classList.remove("show");
            menuToggle.setAttribute("aria-expanded", "false");
        });
    });

    // Close sidebar using Escape
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            sidebar.classList.remove("show");
            menuToggle.setAttribute("aria-expanded", "false");
        }
    });

    // Flash messages
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (message) {
        // Keep the message visible for 4 seconds.
        setTimeout(function () {
            message.classList.add("flash-hiding");

            // Remove it after the fade-out animation.
            setTimeout(function () {
                message.remove();
            }, 400);
        }, 4000);
    });

});

