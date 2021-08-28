var main = document.querySelector('#feature')


i=1;
function addVariant() {
    main.innerHTML += `
    <div class=color>
        <label for='color${i}'> Color: </label>
        <input type='text' name='color${i}' id='color${i}'>

        <label for='Hex code${i}'> Hex code: </label>
        <input type='text' name='Hex code${i}' id='Hex code${i}'>

        <label for='size${i}'> Size: </label>
        <select name='size${i}' id='size${i}' required>
            <option value="XS">XS</option>
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
            <option value="XL">XL</option>
            <option value="XXL">XXL</option>
        </select>   

        <label for='stock${i}'> Stock: </label>
        <input type='number' name='stock${i}' id='stock${i}' min="0">
        <input type='button' value="Discard" onclick="deleteVariant()"></button>
    </div> 
    `
    i ++;
}




//Remove Variant
function deleteVariant() {
    main.addEventListener('click', (event) => {
        if (event.target.value == 'Discard') {
            let divToDelete = event.target.parentNode;
            console.log(divToDelete);
            main.removeChild(divToDelete)
        }
    })
}


