// waits for the DOM to load
$(document).ready(function() {
    pokemon_image = document.getElementById("pokemon-image");

    $(':checkbox').on("change", function(){
        if(this.checked){
            console.log("input checked");
            pokemon_image.src = pokemon_js.shiny_sprites;
        }else{
            console.log("unchecked");
            pokemon_image.src = pokemon_js.sprites;
        }
    })
});