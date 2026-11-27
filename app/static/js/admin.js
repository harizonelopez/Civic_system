document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("adminSidebar");
    const menuToggle = document.getElementById("adminMenuToggle");

    // Sidebar functionality
    if (sidebar && menuToggle) {
        menuToggle.addEventListener("click", function () {
            const isOpen = sidebar.classList.toggle("show");
            menuToggle.setAttribute("aria-expanded", isOpen);
        });

        const navigationLinks = sidebar.querySelectorAll(".admin-nav-link");
        navigationLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                sidebar.classList.remove("show");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                sidebar.classList.remove("show");
                menuToggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    // Flash messages
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.classList.add("flash-hiding");
            setTimeout(function () {
                message.remove();
            }, 400);
        }, 4000);
    });

    // Citizens page: search and account status filtering
    const citizenSearch = document.getElementById("citizenSearch");
    const citizenStatusFilter = document.getElementById("citizenStatusFilter");
    const citizenCards = document.querySelectorAll("[data-citizen-card]");
    const citizenGroups = document.querySelectorAll("[data-citizen-group]");
    const citizenNoResults = document.getElementById("citizenNoResults");

    if (citizenSearch && citizenStatusFilter) {

        function filterCitizens() {
            const searchTerm = citizenSearch.value.trim().toLowerCase();
            const selectedStatus = citizenStatusFilter.value;

            let visibleCount = 0;

            // Filter individual citizen cards
            citizenCards.forEach(function (card) {
                const searchData = card.dataset.search || "";
                const accountStatus = card.dataset.status;

                const matchesSearch = searchData.includes(searchTerm);

                const matchesStatus =
                    selectedStatus === "all" ||
                    accountStatus === selectedStatus;

                const visible = matchesSearch && matchesStatus;

                card.hidden = !visible;

                if (visible) {
                    visibleCount++;
                }
            });

            // Hide sections that have no matching citizens
            citizenGroups.forEach(function (group) {
                const visibleCards = group.querySelectorAll(
                    "[data-citizen-card]:not([hidden])"
                );

                group.hidden = visibleCards.length === 0;
            });

            // Display the no-results message when necessary
            if (citizenNoResults) {
                citizenNoResults.hidden = visibleCount !== 0;
            }
        }

        citizenSearch.addEventListener("input", filterCitizens);
        citizenStatusFilter.addEventListener("change", filterCitizens);

        // Apply initial filtering
        filterCitizens();
    }
});
