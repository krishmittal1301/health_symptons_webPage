// Replace 'YOUR_SERVER_URL' with the actual URL where your Flask app is running
const serverUrl = 'http://localhost:5000';

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;


$(window).load(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
        fakeMessage();
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    // console.log(msg)
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    setTimeout(function () {
        fakeMessage(msg);
    }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
})


function fakeMessage(msg) {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="https://5.imimg.com/data5/SELLER/Default/2023/12/365695679/GL/DU/HU/20619026/9086614aee448043586a422bec08ced0-500x500.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        $('.message.loading').remove();
        const prompt = msg;
        console.log(prompt)

        $.ajax({
            type: 'POST',
            url: `${serverUrl}/generate`,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ prompt: prompt }),
            success: function (response) {
                // Handle the response (generated content)
                console.log(response.generated_content);
                $('<div class="message new"><figure class="avatar"><img src="https://5.imimg.com/data5/SELLER/Default/2023/12/365695679/GL/DU/HU/20619026/9086614aee448043586a422bec08ced0-500x500.jpg" /></figure>' + response.generated_content + '</div>').appendTo($('.mCSB_container')).addClass('new');

            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
        setDate();
        updateScrollbar();
    }, 1000 + (Math.random() * 20) * 100);

}