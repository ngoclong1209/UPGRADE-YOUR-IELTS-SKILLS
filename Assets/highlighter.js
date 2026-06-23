document.addEventListener('DOMContentLoaded', () => {
    // Disable copying
    document.addEventListener('copy', (e) => {
        e.preventDefault();
        return false;
    });
    
    // Disable context menu
    document.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });

    const colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#D0BAFF', '#FFBAE1'];
    
    // Create palette
    const palette = document.createElement('div');
    palette.id = 'youpass-palette';
    palette.style.display = 'none';
    
    colors.forEach(color => {
        const btn = document.createElement('div');
        btn.className = 'youpass-color-btn';
        btn.style.backgroundColor = color;
        btn.addEventListener('mousedown', (e) => {
            e.preventDefault(); // prevent selection loss
            applyHighlight(color);
        });
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            applyHighlight(color);
        });
        palette.appendChild(btn);
    });
    document.body.appendChild(palette);

    // Create remove button
    const removeBtn = document.createElement('div');
    removeBtn.id = 'youpass-remove-btn';
    removeBtn.innerText = '🗑️ Xóa màu';
    removeBtn.style.display = 'none';
    let currentHighlight = null;

    removeBtn.addEventListener('mousedown', (e) => {
        e.preventDefault();
        removeHighlight();
    });
    removeBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        removeHighlight();
    });
    document.body.appendChild(removeBtn);

    let savedRange = null;

    document.addEventListener('selectionchange', () => {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed || sel.toString().trim() === "") {
            palette.style.display = 'none';
        }
    });

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    function handleSelection(e) {
        if (e.target.closest('#youpass-palette') || e.target.closest('#youpass-remove-btn')) return;
        
        // Hide remove button if clicking outside
        if (!e.target.classList.contains('youpass-highlight')) {
            removeBtn.style.display = 'none';
        }

        setTimeout(() => {
            const sel = window.getSelection();
            if (sel && !sel.isCollapsed && sel.toString().trim() !== "") {
                savedRange = sel.getRangeAt(0);
                const rect = savedRange.getBoundingClientRect();
                
                palette.style.display = 'flex';
                palette.style.top = `${window.scrollY + rect.top - 50}px`;
                
                let leftPos = rect.left + (rect.width / 2) - 140; // Approx half of palette width
                if (leftPos < 10) leftPos = 10;
                palette.style.left = `${leftPos}px`;
            } else {
                palette.style.display = 'none';
            }
        }, 50);
    }

    function applyHighlight(color) {
        if (!savedRange) return;
        
        try {
            const span = document.createElement('span');
            span.className = 'youpass-highlight';
            span.style.backgroundColor = color;
            savedRange.surroundContents(span);
        } catch (err) {
            // Complex selection spanning multiple nodes
            const span = document.createElement('span');
            span.className = 'youpass-highlight';
            span.style.backgroundColor = color;
            span.appendChild(savedRange.extractContents());
            savedRange.insertNode(span);
        }
        
        window.getSelection().removeAllRanges();
        palette.style.display = 'none';
        savedRange = null;
    }

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('youpass-highlight')) {
            currentHighlight = e.target;
            const rect = currentHighlight.getBoundingClientRect();
            removeBtn.style.display = 'block';
            removeBtn.style.top = `${window.scrollY + rect.top - 40}px`;
            
            let leftPos = rect.left + (rect.width / 2) - 40;
            removeBtn.style.left = `${leftPos}px`;
        }
    });

    function removeHighlight() {
        if (currentHighlight) {
            const parent = currentHighlight.parentNode;
            while (currentHighlight.firstChild) {
                parent.insertBefore(currentHighlight.firstChild, currentHighlight);
            }
            parent.removeChild(currentHighlight);
            currentHighlight = null;
            removeBtn.style.display = 'none';
        }
    }
});
