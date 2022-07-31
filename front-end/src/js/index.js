// empty

/* Web Socket */


/* Input Button */
let text_input = document.getElementById("user-message");
text_input.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        InputEnter();
    }
})

function InputEnter() {
    console.log(text_input.value);
    CreateMessage("user", text_input.value);
    text_input.value = "";
}

function CreateMessage(from, content) {
    let messages = document.getElementsByClassName("messages")[0];
    if (from == "user") {
        messages.innerHTML +=
            "<div class=\"message\"> \
                <p class=\"message-content\">" + content + "</p> \
            </div>";
    } else if (from == "server") {
        // content = [
        //      type: message,
        //      header: [string],
        //      content: [string]
        // ]
        if (content[0] == "message") {
            headings = "";
            for (let i in content[1]) {
                headings += "<p class=\"message-heading\">" + i + "</p>";
            }
            contents = "";
            for (let i in content[2]) {
                contents += "<p class=\"message-content\">" + i + "</p>";
            }
            messages.innerHTML +=
            "<div class=\"message\">"
                + headings + contents
            "</div>";
        }
    }
}
