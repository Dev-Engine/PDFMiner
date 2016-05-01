/**
 * Created by Scen on 5/1/16.
 */
(function ($) {
    
    $('#pdf_search').click(function (e) {
        e.preventDefault();
        var self = $(this),
            keywords = self.parent().find('input[name=pdf_keywords]').val();
        
        if (keywords.length == 0) return;
        
        $.ajax({
            type: 'POST',
            url: '/pdf/search',
            dataType: 'JSON',
            data: {
                keywords: keywords
            },
            success: function(data) {
                console.log(data)
            }
        })
    })
    
})(window.jQuery);
