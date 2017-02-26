$(function() {
    console.log('running');
    likebutton = $("#likebutton");
    likecount = $("#likecount");
    liked = $("#liked");
    liked.hide();  
    likebutton.click(function(e) {
        e.preventDefault();
        $.ajax({
            url: likebutton.data('url'),
            success: function(data) {
                if (data.status == 200) {
                    var newcount = parseInt($.trim(likecount.text()));
                    likecount.text(++newcount);
                    likebutton.hide();
                    liked.show();
                }
            },
        });
    });
});