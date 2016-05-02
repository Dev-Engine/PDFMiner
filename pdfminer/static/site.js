/**
 * Created by Scen on 5/1/16.
 */
(function ($) {

    const search_tpl = "<a href='' target='_blank'></a><hr/>";
    
    $('form').submit(function (e) {
        e.preventDefault();
        return false;
    });
    
    $('#pdf_search').click(function (e) {
        e.preventDefault();
        var self = $(this),
            keywords = self.parent().find('input[name=pdf_keywords]').val();
        
        if (keywords.length == 0) return;

        self.text('Loading...');
        $('#search_result').empty();
        
        $.ajax({
            type: 'POST',
            url: '/pdf/search',
            dataType: 'JSON',
            data: {
                keywords: keywords
            },
            success: function(data) {
                self.text('Search');
                console.log(data);
                var r = $(search_tpl).clone();
                if (!data.root) {
                    $(r[0])
                        .text(data.Error);
                    r.appendTo('#search_result');
                } else {
                    for (var i = 0; i < data.root.document.length; i ++) {
                        $(r[0])
                            .attr('href', data.root.document[i].mdurl)
                            .text(data.root.document[i].pubtitle);
                        r.appendTo('#search_result');
                    }
                }
            }
        })
    })
    
})(window.jQuery);
