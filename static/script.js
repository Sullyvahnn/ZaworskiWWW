
    var lastMessageID = null; // global variable, we will save the ID of the last received message here
    var loadMessagesTimeout = null; // global viariable, we will save the timer from loadMessages() here

    function loadMessages() {
        clearTimeout(loadMessagesTimeout);

        $.ajax({
            url: "/chat/messages",
            type: "GET",
            dataType: "json",
            data: {
                'message_id': lastMessageID
            },
        })
        .done(function( data ) {
            jQuery.each(data['result'], function() {
                lastMessageID = this.id;
                console.log(this.id, this.username, this.content, this.created_at);
                appendMessageToChatWindow(
                    this.id,
                    this.username,
                    this.content,
                    this.created_at,
                    (currentUserID == this.user_id ? true : false)
                )
                $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
            });
            loadMessagesTimeout = setTimeout(loadMessages, 10000);
        })
        .fail(function( xhr, status, errorThrown ) {
            alert("Cannot load messages.");
        });
    }

    // creates HTML code for the message and adds it to the chat window
    // argument "editable" should be set to true if user is the author of the message
    function appendMessageToChatWindow(messageID, username, content, created_at, editable) {
        let buttons = `<span class="edit-button" onclick="editMessageOpenWindow(${messageID});">&#9998;</span>
                       <span class="delete-button" onclick="deleteMessage(${messageID})">&#10005;</span>`;

        // We use the .append() function to add message HTML to the chat window.
        $('#chat-window').append(`<div id="message-${messageID}">
                                    <span style="font-weight: bold;">[${created_at}]
                                    <span style="color: #ecd03a;">${username}</span></span>:
                                    <span id="message-content-${messageID}"></span>
                                    ${editable ? buttons : ''}
                                  </div>`)

        // We did not insert the message content with .append(), but we are doing it now using
        // text() because .append() is vulnerable to XSS attacks.
        // https://owasp.org/www-community/attacks/xss/
        $(`#message-content-${messageID}`).text(content);
    }



    function editMessageOpenWindow(messageID) {
        console.log("Opening window for message " + messageID);
        let messageContent = $(`#message-content-${messageID}`).text(); // get message content from chat window
        $('#editMessageModal .editMessageID').text(messageID); // set message ID in modal
        $('#editMessageModal .editMessageContent').val(messageContent); // set message content in modal
        $('#editMessageModal').modal('show'); // open modal
    }

    function editMessageSave() {
        let messageID = $('#editMessageModal .editMessageID').text(); // get message ID from modal
        let messageContent = $('#editMessageModal .editMessageContent').val(); // get message content from modal

        if (!messageContent) {
            alert('No content given.');
            return false;
        }

        console.log(`Saving message ${messageID}`);
        console.log(`New content: ${messageContent}`);

        $.ajax({
            url: `/chat/messages/${messageID}`,
            type: "PUT",
            data: JSON.stringify({
                'content': messageContent
            }),
            contentType: "application/json",
        })
        .done(function( data ) {
            $(`#message-content-${messageID}`).text(messageContent);
            $('#editMessageModal').modal('hide');
        })
        .fail(function( xhr, status, errorThrown ) {
            alert("Cannot edit message.");
        });
    }

    function deleteMessage(messageID) {
        console.log(`Deleting message ${messageID}`);

        $.ajax({
            url: `/chat/messages/${messageID}`,
            type: "DELETE",
        })
        .done(function( data ) {
            $(`#message-${messageID}`).remove();
        })
        .fail(function( xhr, status, errorThrown ) {
            alert("Cannot delete message.");
        });
    }


 function addMessage() {
        let content = $('#message-input').val(); // get message content

        if (content) {
            console.log(`Adding message: ${content}`);
        } else {
            alert("No message given.");
            return false;
        }

        $.ajax({
            url: "/chat/messages",
            type: "POST",
            data: JSON.stringify({
                'content': content
            }),
            contentType: "application/json",
        })
        .done(function( data ) {
            $('#message-input').val('');
            loadMessages();
        })
        .fail(function( xhr, status, errorThrown ) {
            alert("Cannot add message.");
        });
    }


    $().ready(function() {
        // initialize chat and load messages
        loadMessages();
    });