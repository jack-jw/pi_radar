document.addEventListener("DOMContentLoaded", function() {
    let isResizing = false;
    let startY = 0;
    let startHeight = 0;
    const minHeight = 80;
    
    const container = document.querySelector(".main-container");
    
    let elements = container.children;
    let maxHeight = 60;
    let i = 0;
    
    for (i = 0; i < elements.length; i++) {
        maxHeight += elements[i].offsetHeight;
    }
    
    container.addEventListener("touchstart", startResize);
    
    document.addEventListener("touchmove", resize);
    
    container.addEventListener("wheel", scrollResize);
    
    document.addEventListener("touchend", stopResize);
    
    function startResize(e) {
        isResizing = true;
        startY = e.clientY || e.touches[0].clientY;
        startHeight = container.clientHeight;
        e.preventDefault();
    }
    
    function resize(e) {
        if (isResizing) {
            let deltaY = (e.clientY || e.touches[0].clientY) - startY;
            newHeight = startHeight - deltaY;
            if (newHeight >= minHeight && newHeight <= maxHeight) {
                container.style.height = newHeight + "px";
            } else if (newHeight < minHeight) {
                container.style.height = minHeight + "px";
            } else if (newHeight > maxHeight) {
                container.style.height = maxHeight + "px";
            }
            e.preventDefault();
        }
    }
    
    function scrollResize(e) {
        let delta = e.deltaY;
        let newHeight = container.clientHeight + delta;
        if (newHeight >= minHeight && newHeight <= maxHeight) {
            container.style.height = newHeight + "px";
        } else if (newHeight < minHeight) {
            container.style.height = minHeight + "px";
        } else if (newHeight > maxHeight) {
            container.style.height = maxHeight + "px";
        }
        e.preventDefault();
    }
    
    function stopResize() {
        isResizing = false;
    }
});


