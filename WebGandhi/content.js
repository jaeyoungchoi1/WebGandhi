function checkForElements() {
    const elements = document.querySelectorAll('.usertxt.ub-word');
    if (elements.length > 0) {
        alert('[WebGandhi] Hate Speech Detected!');
    }
}

window.addEventListener('load', checkForElements);