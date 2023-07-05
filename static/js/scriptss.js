let current_state = "description";
        let previous_answers = {};
    
        $(document).ready(function() {
            $('#userInputForm').on('submit', function(e) {
                e.preventDefault();
    
                let userText = $('#userInput').val();
                $('#chatbox').append('<div class="messageContainer"><p class="userMessage">User: ' + userText + '</p></div>');
                $('#userInput').val("");
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
    
                $('#chatbox').append('<div id="loadingMessage" class="messageContainer"><p class="botMessage2">Bot: Generating your advertisement <span class="typing-indicator"><span></span><span></span><span></span></span>  </p></div>');
                
                getBotResponse(userText);
            });
        });
    
        function getBotResponse(userInput) {
            $.ajax({
                url: '/chat',
                data: JSON.stringify({ 
                    'user_input': userInput,
                    'previous_answers': previous_answers,
                    'current_state': current_state
                }),
                contentType: 'application/json',
                type: 'POST',
                success: function(response) {
                    current_state = response['next_state'];
                    previous_answers = response['previous_answers'];
                    
                    $('#loadingMessage').remove();
                    let botHtml = '<div class="messageContainer"><p class="botMessage">Bot: ' + response['question'] + '</p></div>';
                    $('#chatbox').append(botHtml);
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                },
                error: function(error) {
                    console.log(error);
                    $('#loadingMessage').remove();
                    let botHtml = '<div class="messageContainer"><p class="botMessage">Bot: Sorry, something went wrong while generating your advertisement. Please try again.</p></div>';
                    $('#chatbox').append(botHtml);
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                }
            });
        }