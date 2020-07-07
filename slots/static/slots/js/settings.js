var form = document.getElementsByClassName('settings')[0];
for (var child of form.children) {
    if (child.tagName.toLowerCase() === 'input' && child.type.toLowerCase() != 'submit' && child.type.toLowerCase() != 'hidden') {
        child.value = '';
    }
}
