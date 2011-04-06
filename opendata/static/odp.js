$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    if (window.location.search == "") {return vars;}
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var odp = {
    tags: null,

    setupSearchInput: function () {
        $("#qs").focus(function (evt) {
            if (this.value == "Search for data") {
                this.value = "";
            }
        });
        $("#qs").focusout(function (evt) {
            if(this.value == "") {
                this.value = "Search for data";
            }
        });
    },

    setupSortLinks: function () {
        if (window.location.search == "") {
            $("#sort_name").attr("href", location.href + "?sort=name&dir=asc");
            $("#sort_rating").attr("href", location.href + "?sort=rating&dir=asc");
            return;
        }
        
        $("#sort_name").css('background_position', 'center bottom');
        $("#sort_rating").css('background_position', 'center bottom');
        
        var dir = "";
        ($.getUrlVar('dir')=='asc') ? dir = 'desc' : dir = 'asc';
        
        if ($.getUrlVar('sort') == 'name') {
            $("#sort_name").attr("href", location.href.split(location.search)[0] + "?sort=name&dir=" + dir).css("background-position", "top center");
            $("#sort_rating").attr("href", location.href.split(location.search)[0] + "?sort=rating&dir=asc");
        }
        else if ($.getUrlVar('sort') == 'rating') {
            $("#sort_rating").attr("href", location.href.split(location.search)[0] + "?sort=rating&dir=" + dir).css("background-position", "top center");
            $("#sort_name").attr("href", location.href.split(location.search)[0] + "?sort=name&dir=asc");
        }
    },

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