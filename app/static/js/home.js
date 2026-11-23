document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("serviceSearch");
    const searchButton = document.getElementById("searchServices");
    const cards = document.querySelectorAll(".service-card-item");
    const emptyMessage = document.getElementById("noServicesFound");

    if (!searchInput || !searchButton || !emptyMessage) {
        return;
    }

    function filterServices() {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        cards.forEach(function (card) {
            const searchableText = (
                card.dataset.search + " " + card.textContent
            ).toLowerCase();

            const matches = searchableText.includes(query);
            card.classList.toggle("d-none", !matches);

            if (matches) {
                visibleCount++;
            }
        });

        emptyMessage.classList.toggle("d-none", visibleCount > 0);
    }

    searchInput.addEventListener("input", filterServices);
    searchButton.addEventListener("click", filterServices);
    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            filterServices();
        }
    });
});
