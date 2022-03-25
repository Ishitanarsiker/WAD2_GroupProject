$(document).ready(function() {
   $('#like_btn').click(function() {
        var lectureIdVar;
        lectureIdVar = $(this).attr('data-lectureid');

        $.get('/lectureFinderApp/like_lecture/',
            {'lecture_id': lectureIdVar}, function(data) {
                $('#like_count').html("Likes: " + data);
                $('#like_btn_container').hide();
            })
   });
});
