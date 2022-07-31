// empty

/* Web Socket */
let socket = new WebSocket("ws://localhost:8000/ws");
socket.onopen = (event) => {
    alert("[Connection Established]");
};
socket.onmessage = (event) => {
    if (event.data == "connected") return;
    console.log(event.data);
    let event_data = JSON.parse(event.data);
    console.log(event_data);
    if (event_data.source != "s") return;
    
    if (event_data.type == "ws_setup") {
        window.uuid = event_data.content;
    }
};

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
    socket.send(text_input.value);
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
