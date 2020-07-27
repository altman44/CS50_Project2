document.querySelectorAll('.toggler-options-arrow').forEach(toggler => {
    toggler.addEventListener('click', function() {
        this.classList.toggle('collapse-options-arrow');
        const hiddenContent = document.querySelector(this.dataset.target);
        console.log(hiddenContent);
        hiddenContent.classList.toggle('expand');
    })
})