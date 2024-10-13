function toggleCommentBox(button) {
    const commentBox = button.nextElementSibling;
    const imageInput = commentBox.querySelector('#imageInput');  // campo de input da imagem

    // Mostra o campo de input de imagem quando a caixa de comentários é exibida
    if (commentBox.style.display === 'none' || commentBox.style.display === '') {
        commentBox.style.display = 'block';

        // Mostra o campo de input de imagem se estiver oculto
        if (imageInput.style.display === 'none') {
            imageInput.style.display = 'block';
        }
    } else {
        commentBox.style.display = 'none';
    }
}
