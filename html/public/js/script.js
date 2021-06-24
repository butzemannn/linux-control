$(document).ready(function(){
    $("button").click(function(){
        $.get("index.php", {
            run: true
        }, (response) => {
            console.log(response)
        });
    });
});