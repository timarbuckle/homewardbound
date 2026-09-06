document.addEventListener("DOMContentLoaded", function () {
    const catTable = document.querySelector("#cat-table");
    if (catTable) {
        const targetUrl = catTable.dataset.url;
        htmx.ajax("GET", targetUrl, "#cat-table");
    }
});

// Image Modal Functions
function openImageModal(src, name) {
    const modal = document.getElementById('image-modal');
    const img = document.getElementById('modal-image');

    img.src = src;
    img.alt = name;

    modal.classList.remove('hidden');
    modal.classList.add('flex');

    // Small timeout allows the display:flex to apply before fading in opacity
    setTimeout(() => modal.classList.remove('opacity-0'), 10);

    // Prevent background scrolling while modal is open
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.getElementById('image-modal');
    modal.classList.add('opacity-0');

    // Wait for the fade-out transition to finish before hiding
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.style.overflow = 'auto'; // Restore scrolling
    }, 300);
}

// Close modal if user presses the Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && !document.getElementById('image-modal').classList.contains('hidden')) {
        closeImageModal();
    }
  });
