document.addEventListener("DOMContentLoaded", function () {
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
