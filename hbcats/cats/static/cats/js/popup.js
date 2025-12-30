document.addEventListener('DOMContentLoaded', () => {
  const tableContainer = document.querySelector('table').parentElement; // Use the table's parent container

  if (!tableContainer) return;

  let activePopup = null; // Track the currently active popup

  const createPopup = () => {
    const popup = document.createElement('div');
    popup.classList.add('image-popup');
    const img = document.createElement('img');
    popup.appendChild(img);
    document.body.appendChild(popup);
    return popup;
  };

  const showPopup = (popup, imageUrl, x, y) => {
    // console.log('Showing popup for image:', imageUrl); // Debug log

    const gap = 20;
    const pageWidth = window.innerWidth;
    const pageHeight = window.innerHeight;

    const img = popup.querySelector('img');
    img.src = imageUrl;

    popup.style.display = 'block';
    popup.style.position = 'absolute'; // Ensure absolute positioning

    const popupWidth = popup.offsetWidth;
    const popupHeight = popup.offsetHeight;

    let posX = x + gap;
    let posY = y + gap;

    // Adjust position to keep the popup within the viewport
    if (posX + popupWidth > pageWidth) {
      posX = x - popupWidth - gap;
    }

    if (posY + popupHeight > pageHeight) {
      posY = y - popupHeight - gap;
    }

    popup.style.left = `${Math.max(posX, 0)}px`;
    popup.style.top = `${Math.max(posY, 0)}px`;
  };

  const hidePopup = (popup) => {
    // console.log('Hiding popup'); // Debug log
    popup.style.display = 'none';
  };

  if (!activePopup) {
    activePopup = createPopup();
  }

  tableContainer.addEventListener('mouseover', (e) => {
    const target = e.target.closest('.hover-container');
    if (!target) {
      console.log('No hover-container found'); // Debug log
      return;
    }

    const imageUrl = target.getAttribute('data-image-url');
    if (!imageUrl) {
      console.log('No data-image-url found'); // Debug log
      return;
    }

    showPopup(activePopup, imageUrl, e.pageX, e.pageY);
  });

  tableContainer.addEventListener('mousemove', (e) => {
    const target = e.target.closest('.hover-container');
    if (!target) {
      console.log('No hover-container found on mousemove'); // Debug log
      return;
    }

    const imageUrl = target.getAttribute('data-image-url');
    if (!imageUrl) {
      console.log('No data-image-url found on mousemove'); // Debug log
      return;
    }

    showPopup(activePopup, imageUrl, e.pageX, e.pageY);
  });

  tableContainer.addEventListener('mouseout', (e) => {
    const target = e.target.closest('.hover-container');
    if (!target) {
      console.log('No hover-container found on mouseout'); // Debug log
      return;
    }

    hidePopup(activePopup);
  });

  // Observe changes to the table and log them
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes.length > 0) {
        console.log('DOM changes detected:', mutation.addedNodes); // Debug log
      }
    });
  });

  observer.observe(tableContainer, { childList: true, subtree: true });
});