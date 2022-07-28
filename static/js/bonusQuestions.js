// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        items.sort((a,b)=> {
            a = a["Description"];
            b = b["Description"];
            if(a<b){
                return -1;
            }
            if(a>b){
                return 1;
            } else {
                return 0;
            }
        })
    } else {
        items.sort((a,b)=> {
            a = a["Description"];
            b = b["Description"];
            if(a<b){
                return 1;
            }
            if(a>b){
                return -1;
            } else {
                return 0;
            }
        })
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    fontEval(1);
}

function decreaseFont() {
    fontEval(-1);
}

function fontEval(modNum){
    let tableRows = document.querySelectorAll("tr")
    for (const tableRow of tableRows) {
        let number = window.getComputedStyle(tableRow, null).getPropertyValue("font-size")
        console.log(number)
        let fontSize = Number(number.replace("px", ""))
        const limit = modNum > 0 ? 15 : 3;
        if (modNum > 0) {
            fontSize = fontSize < limit ? fontSize + 1 * modNum : fontSize;
        } else {
            fontSize = fontSize > limit ? fontSize + 1 * modNum : fontSize;
        }
        tableRow.setAttribute("style", `font-size: ${fontSize}px`)
    }

}