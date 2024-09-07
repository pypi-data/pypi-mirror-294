function SpaceBlocks( elements, pageHeight, overflow = 0 ) {
    var elementsHeight = 0;
    for ( var i = 0; i < elements.length; i++ ) {
        elementsHeight += elements[i].scrollHeight;
    }
    if ( overflow > 0 ) {
        elementsHeight += overflow;
    }
    console.log( "Total element list height = " + elementsHeight );
    var paddingBottom = Math.floor(40 / elements.length)
    if ( elements.length > 0 && (pageHeight - elementsHeight) > (paddingBottom + 1 + elements.length) ) {
        var space = Math.ceil( ( pageHeight - elementsHeight - paddingBottom ) / (1 + elements.length) );
        for ( var e = 0; e < elements.length; e++ ) {
            var spacing = document.createElement("div");
            spacing.setAttribute( "id", "centerspacing" );
            spacing.style.height = space;
            elements[e].insertAdjacentElement( "afterbegin", spacing );
            console.log( "Added " + spacing.scrollHeight + "px spacing before '" + elements[e].getAttribute("name") + "'" );
        }
    }
}

window.addEventListener( 'beforeprint', (event) => {
    var content = document.getElementById("content");
    var headerFooterHeight = ( document.getElementById("heading").scrollHeight + document.getElementById("heading").scrollHeight );
    console.log( "headerFooterHeight = " + headerFooterHeight + "px" );
    var availableHeight = ( 842 - headerFooterHeight );
    console.log( "availableHeight = " + availableHeight + "px" );
    var numberOfPages = 1;
    var blocks = document.querySelectorAll("[id^=block], [id^=image-block], [class^=pagebreak]");
    var pageElements = [];
    var overflow = 0;
    for ( var i = 0; i < blocks.length; i++ ) {
        var pageHeight = overflow;
        for ( var p = 0; p < pageElements.length; p++ ) {
            pageHeight += pageElements[p].scrollHeight;
        }
        var cls = blocks[i].getAttribute("class");
        if ( cls == "pagebreak" ) {
            console.log( "Adding page due to pagebreak div. Number of pages: " + numberOfPages );
            if ( pageElements.length > 0 ) {
                console.log( "Spacing " + pageElements.length + " elements across page #" + numberOfPages );
                SpaceBlocks( pageElements, availableHeight, overflow );
                var pageElements = [];
            }
            numberOfPages += 1;
            var pageHeight = 0;
            continue;
        }
        var name = blocks[i].getAttribute("name");
        var blockHeight = blocks[i].scrollHeight;
        console.log( "Block " + i + " ('" + name + "') height = " + blockHeight + "px" );
        if ( pageElements.length == 0 && blockHeight > availableHeight ) {
            console.log( "Element height " + blockHeight + " is larger than available " + availableHeight );
            while ( blockHeight > availableHeight ) {
                numberOfPages += 1;
                console.log( "Added page #" + numberOfPages + " for element '" + name + "'" );
                blockHeight -= availableHeight;
            }
            var overflow = blockHeight;
            console.log( "Page #" + numberOfPages + " pageHeight: " + pageHeight + "px" );
        } else if ( (pageHeight + blockHeight) > availableHeight ) {
            numberOfPages += 1;
            console.log( "Spacing " + pageElements.length + " elements across page #" + numberOfPages );
            SpaceBlocks( pageElements, availableHeight, overflow );
            var pageElements = [];
            if ( blockHeight > availableHeight ) {
                console.log( "Element height " + blockHeight + " is larger than available " + availableHeight );
                while ( blockHeight > availableHeight ) {
                    numberOfPages += 1;
                    console.log( "Added page #" + numberOfPages + " for element '" + name + "'" );
                    blockHeight -= availableHeight;
                }
                var overflow = blockHeight;
                console.log( "Page #" + numberOfPages + " pageHeight: " + pageHeight + "px" );
            } else {
                pageElements.push( blocks[i] );
                var overflow = 0;
            }
        } else {
            pageElements.push( blocks[i] );
            pageHeight += blockHeight
            console.log( "Added element '" + name + "' to Page #" + numberOfPages + " - Total page height: " + pageHeight + "px" );
        }
    }
    if ( pageElements.length > 0 ) {
        console.log( "Spacing " + pageElements.length + " elements across page #" + numberOfPages );
        SpaceBlocks( pageElements, availableHeight, overflow );
    } else {
        console.log( "Removing blank page from end of document" );
        numberOfPages -= 1;
    }
    console.log( "Total number of pages: " + numberOfPages );
    for ( var i = 1; i <= numberOfPages; i++ ) {
        var pageNumberDiv = document.createElement("div");
        var pageNumber = document.createTextNode("Page " + i + " of " + numberOfPages );
        pageNumberDiv.setAttribute( "id", "pagenum" );
        pageNumberDiv.style.zIndex = "1000";
        pageNumberDiv.style.marginTop = "calc((" + i + " * 11in) - 10.9in)"; //"calc((" + i + " * (297mm - 0.5px)) - 40px)"; //297mm A4 pageheight; 0,5px unknown needed necessary correction value; additional wanted 40px margin from bottom(own element height included)
        pageNumberDiv.appendChild(pageNumber);
        // document.body.insertBefore(pageNumberDiv, document.getElementById("content"));
        document.body.insertBefore(pageNumberDiv, content);
        pageNumberDiv.style.left = "calc(100% - (" + pageNumberDiv.offsetWidth + "px + 20px"; //"px + 20px))";
    }
});
