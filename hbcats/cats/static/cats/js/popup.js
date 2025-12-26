  document.addEventListener('DOMContentLoaded', () => {
  const containers = document.querySelectorAll('.hover-container');

  containers.forEach(container => {
    const popup = container.querySelector('.popup-image');
    
    if (!popup) return; // Skip if no popup found in this container

    container.addEventListener('mousemove', (e) => {
      // Make visible
      popup.style.display = 'block';

      const gap = 20;
      const pageWidth = window.innerWidth;
      const pageHeight = window.innerHeight;
      
      // Get the size of the popup image
      const popupWidth = popup.offsetWidth;
      const popupHeight = popup.offsetHeight;

      // Calculate position
      let x = e.clientX + gap;
      let y = e.clientY + gap;

      // Flip left if it hits the right edge
      if (x + popupWidth > pageWidth) {
        x = e.clientX - popupWidth - gap;
      }

      // Shift up if it hits the bottom edge
      if (y + popupHeight > pageHeight) {
        y = e.clientY - popupHeight - gap;
      }

      // Final boundary check for top/left
      if (x < 0) x = gap;
      if (y < 0) y = gap;

      popup.style.left = x + 'px';
      popup.style.top = y + 'px';
    });

    container.addEventListener('mouseleave', () => {
      popup.style.display = 'none';
    });
  });
});