document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("directorySearch");
    const filterButtons = document.querySelectorAll(".filter-btn");
    const serviceItems = document.querySelectorAll(".service-directory-item");
    const emptyState = document.getElementById("directoryEmpty");
    const clearButton = document.getElementById("clearDirectorySearch");
    const serviceCount = document.getElementById("serviceCount");

    if (!searchInput || !emptyState || !serviceCount) {
        return;
    }

    let activeCategory = "all";

    function filterServices() {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        serviceItems.forEach(function (item) {
            const category = item.dataset.category.toLowerCase();
            const searchableText = item.dataset.search.toLowerCase();
            const matchesCategory =
                activeCategory === "all" || category === activeCategory;
            const matchesSearch = searchableText.includes(query);
            const isVisible = matchesCategory && matchesSearch;
            item.classList.toggle("d-none", !isVisible);
            if (isVisible) {
                visibleCount++;
            }
        });

        serviceCount.textContent = visibleCount;
        emptyState.classList.toggle("d-none", visibleCount > 0);
    }

    // Search services as the user types
    searchInput.addEventListener("input", filterServices);

    // Category filtering
    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            filterButtons.forEach(function (filterButton) {
                filterButton.classList.remove("active");
            });
            button.classList.add("active");

            activeCategory = button.dataset.category.toLowerCase();
            filterServices();
        });
    });

    // Clear search and reset category filters
    clearButton.addEventListener("click", function () {
        searchInput.value = "";
        activeCategory = "all";

        filterButtons.forEach(function (button) {
            button.classList.toggle(
                "active",
                button.dataset.category === "all"
            );
        });

        filterServices();
    });
});
