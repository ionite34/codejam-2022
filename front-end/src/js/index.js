// empty

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
    if (from == "user") {
        let messages = document.getElementsByClassName("messages")[0];
        messages.innerHTML += 
            "<div class=\"message\"> \
                <p class=\"message-content\">" + content + "</p> \
            </div>";
    }
}