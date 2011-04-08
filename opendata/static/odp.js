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
        if ($.getUrlVar('qs') && $.getUrlVar('qs') != "") {
            $("#qs")[0].value = decodeURI($.getUrlVar('qs'));
        }
    
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
        
        $("#search_form").submit(function(evt) {
            if ($("#qs")[0].value != "" | $("#qs")[0].value != "Search for data")
            evt.stopImmediatePropagation();
            evt.preventDefault();
            window.location = "/opendata/search/?qs=" + decodeURI($("#qs")[0].value);
            
        });
        
    },

    setupSortLinks: function () {
        //TODO: fix usage with a search string
        if ($.getUrlVar('sort')!='name' && $.getUrlVar('sort') != 'rating_score') {
            $("#sort_name").attr("href", location.href + "?sort=name&dir=asc");
            $("#sort_rating").attr("href", location.href + "?sort=rating_score&dir=desc");
            return;
        }
        
        $("#sort_name").css('background_position', 'center bottom');
        $("#sort_rating").css('background_position', 'center bottom');
        
        var dir = "";
        ($.getUrlVar('dir')=='asc') ? dir = 'desc' : dir = 'asc';
        
        if ($.getUrlVar('sort') == 'name') {
            $("#sort_name").attr("href", location.href.split(location.search)[0] + "?sort=name&dir=" + dir).addClass('active');
            $("#sort_rating").attr("href", location.href.split(location.search)[0] + "?sort=rating_score&dir=desc");
        }
        else if ($.getUrlVar('sort') == 'rating_score') {
            $("#sort_rating").attr("href", location.href.split(location.search)[0] + "?sort=rating_score&dir=" + dir).addClass('active');
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