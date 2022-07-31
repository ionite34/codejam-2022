// empty

/* Web Socket */
let websocket = new WebSocket("ws://localhost:8000/ws");
websocket.onopen = (event) => {
    alert("[Connection Established]");
    CreateMessage("message", ["Connection Established"], []);
};
websocket.onmessage = (event) => {
    if (event.data == "connected") return;
    console.log(event.data);
    let event_data = JSON.parse(event.data);
    
    if (event_data.source == "c") {
        if (event_data.type == "ws-setup") {
            window.uuid = event_data.content;
            CreateMessage("message", [], [`UUID: ${uuid}`]);
        }
        
        if (event_data.type == "room-join-s") {
            CreateMessage("message", [`Room ${event_data.content} Joined`], []);
        } if (event_data.type == "room-join-f") {
            CreateMessage("message", [`Could not join Room ${event_data.content}`], []);
        }
    } else {
        if (event_data.type == "room-message") {
            CreateMessage(
                "message",
                [],
                [`>${event_data.source} > ${event_data.content}`]
            )
        }
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
    // test
    if (text_input.value == "CREATE ROOM") {
        send_message = {
            "source": uuid,
            "type": "room-create",
            "content": ""
        };
        websocket.send(JSON.stringify(send_message));
        text_input.value = "";
        return;
    } if (text_input.value.slice(0, 4) == "JOIN") {
        send_message = {
            "source": uuid,
            "type": "room-join",
            "content": text_input.value.slice(5, text_input.value.length)
        }
        websocket.send(JSON.stringify(send_message));
        text_input.value = "";
        return;
    }

    CreateMessage("message", [], [text_input.value]);
    websocket.send(JSON.stringify({
        "source": uuid,
        "type": "room-message",
        "content": text_input.value
    }));
    text_input.value = "";
}

function CreateMessage(type, header, content) {
    let messages = document.getElementsByClassName("messages")[0];
    // content = [
    //      type: message,
    //      header: [string],
    //      content: [string]
    // ]
    if (type == "message") {
        headings = "";
        if (header.length > 0) {
            for (let i of header) {
                headings += "<p class=\"message-heading\">" + i + "</p>";
            }
        }
        contents = "";
        if (content.length > 0) {
            for (let i of content) {
                contents += "<p class=\"message-content\">" + i + "</p>";
            }
        }
        messages.innerHTML +=
        "<div class=\"message\">"
            + headings + contents
        "</div>";
    }
}
