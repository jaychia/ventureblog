$(function() {
    console.log('running');
    likebutton = $("#likebutton");
    likecount = $("#likecount");
    likebutton.click(function(e) {
        e.preventDefault();
        $.ajax({
            url: likebutton.data('url'),
            success: function(data) {
                if (data.status == 200) {
                    var newcount = parseInt($.trim(likecount.text()));
                    likecount.text(++newcount);
                    likebutton.prop('disabled', true);
                }
            },
        });
    });
});