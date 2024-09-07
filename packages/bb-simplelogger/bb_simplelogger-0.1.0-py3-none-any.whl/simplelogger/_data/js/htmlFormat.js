window.addEventListener( "afterprint", (event) => {
    var pagenums = document.querySelectorAll("[id^=pagenum]");
    for ( var i = 0; i < pagenums.length; i += 1 ){
        pagenums[i].remove();
    }
    var spacings = document.querySelectorAll("[id^=centerspacing]");
    for ( var i = 0; i < spacings.length; i += 1 ){
        spacings[i].remove();
    }
});
