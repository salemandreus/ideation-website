const titleInput = document.querySelector('input[name=title');
const slugInput = document.querySelector('input[name=slug]');

const slugify = (val) => {
    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and-') // replacing & with '-and-'
        .replace(/[\s\W-]+/g, '-') //replcaing spaces, non-word chars and dashes with a single '-'
};

titleInput.addEventListener('keyup', (e) => {
    slugInput.setAttribute('value', slugify(titleInput.value));
});