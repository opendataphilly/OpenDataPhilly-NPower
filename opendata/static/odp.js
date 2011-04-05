var odp = {
    tags: null,

    getTags: function() {
        $.getJSON('/tags/', function(tags){
            odp.tags = tags;
            odp.setupTagList();
        });
    },

    setupTagList: function() {
        if (!odp.tags) {return;}
        var tag_list = "";
        for(var i = 0; i < odp.tags.length; i++) {
            var tag = odp.tags[i];
            tag_list += "<li><a class='tag' href='/opendata/tag/" + tag.pk + "'>" + tag.fields.tag_name + "</a></li>"
        }
        $("#tag_list").replaceWith(tag_list);
    }


}