///// chat logic 
function get_linear_message() {
    var history_messages_count = $("#num-messages-select").val()
    var liner_messages = $("#messages .message").slice(-(history_messages_count * 2 + 1))


    var messages = []
    liner_messages.each(function (i, e) {
        messages.push({
            "role": $(this).attr('class').includes('assistant') ? 'assistant' : 'user',
            "content": $(this).text()
        })
    });
    return messages
}

async function stream_message_respone(text) {
    console.log(text)
    // skip special token
    if (text.includes("<|user|>") || text.includes("<|assistant|>")) return;

    // add message
    text = text.replace("<|end|>", "")
    var last_message = $("#messages .message").last()
    if (last_message.attr('class').includes('assistant-message')) {
        last_message.append(text)
    } else {
        $("#messages").append($("<div/>", {
            class: "message assistant-message",
            text: text
        }))
    }

}


async function send_messages(messages) {
    const response = await fetch('http://localhost/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: [JSON.stringify(messages)]
    });

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }

    // Xử lý stream dữ liệu
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let full_text = ""
    while (true) {
        const { done, value } = await reader.read();

        if (done) {
            break;
        }

        stream_message_respone(decoder.decode(value));
    }
}


async function submit_message() {
    var message = $("#user-input").val()
    if (message) {
        // push to chat
        $("#messages").append($("<div/>", {
            class: "message user-message",
            text: message
        }))

        var messages = get_linear_message()
        console.log(messages)

        $("#user-input").val("").focus().select(); // clear and focus on input field
        $(".chat-container").scrollTop($("#messages")[0].scrollHeight);


        await send_messages(messages)
    }
}


$("#send-btn").click(function () {
    submit_message()
})
$('#user-input').keypress(function (event) {
    if (event.which === 13) { // 13 is the key code for 'Enter'
        submit_message()
    }
});