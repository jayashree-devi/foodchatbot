$(document).ready(function () {
    $(document).on('click', '#send_button', function (e) {
        e.preventDefault();
        sendMessage();
    });

    $(document).on('click', '.food_choice', function () {
        sendMessage($(this).text());
    });

    $(document).on('keypress', '#chat_message', function (e) {
        if (e.which === 13) {
            e.preventDefault();
            sendMessage();
        }
    });
});
async function sendMessage(message = '') {
    if($.trim(message) == '' ){
        message = $("#chat_message").val();
    }
    $('#chat_message').val("");
    if($.trim(message) != ''){
        var user_message = '<p class="user-message"><b class="user-name">You: </b>'+message+'</p>';
        $('#chatbotbox').append(user_message);
        var bot_response = $.ajax({
            url: "/food_chatbot/chat",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ message: message }),
            success: function(response) {

            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
        const data = await bot_response;
        var bot_message = '<p class="bot-message"><b class="bot-name">FoodBot: </b>'+data.response+'</p>';
        $('#chatbotbox').append(bot_message);
        $("#chatbotbox").animate({ scrollTop: $('#chatbotbox').prop("scrollHeight")}, 1000);
    }
}