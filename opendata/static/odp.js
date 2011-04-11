var odp = {
    tags: null,

    setupSearchInput: function () {
        if ($.query.get('qs') && $.query.get('qs') != "") {
            $("#qs")[0].value = decodeURI($.query.get('qs'));
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
        var sort_name = $("#sort_name > a").addClass("url_image")[0];
        sort_name.innerHTML = '';
        
        var sort_rating = $("#sort_rating_score > a").addClass("url_image")[0];
        sort_rating.innerHTML = '';
        
        if ($.query.get('sort')) {
            st = $.query.get('sort');
            $("#sort_" + st + " > a")[0].style.backgroundPosition="0 -45px";
        }
        
        $("#sort .url_image").each(function () {
            $(this).hover(function() {
                this.style.backgroundPosition="0 -89px";
            }, function () {
                var filter_split = this.parentNode.id.split('sort_');
                if ($.query.get('sort') && $.query.get('sort') == filter_split[1]) {
                    this.style.backgroundPosition="0 -45px";
                } else {
                    this.style.backgroundPosition="0 0";
                }
            });
        });
    },
    
    setupFilterLinks: function () {
        var filter_api = $("#filter_api > a").addClass("url_image")[0];
        filter_api.innerHTML = '';
        
        var filter_data = $("#filter_data > a").addClass("url_image")[0];
        filter_data.innerHTML = '';
        
        var filter_application = $("#filter_application > a").addClass("url_image")[0];
        filter_application.innerHTML = '';
        
        if ($.query.get('filter')) {
            st = $.query.get('filter');
            $("#filter_" + st + " > a")[0].style.backgroundPosition="0 -45px";
        }
        $("#filter .url_image").each(function () {
            $(this).hover(function() {
                this.style.backgroundPosition="0 -89px";
            }, function () {
                var filter_split = this.parentNode.id.split('filter_');
                if ($.query.get('filter') && $.query.get('filter') == filter_split[1]) {
                    this.style.backgroundPosition="0 -45px";
                } else {
                    this.style.backgroundPosition="0 0";
                }
            });
        });
    },
    
    getFiltered: function (value) {
        if ($.query.get('filter') == value) {
            var newQuery = "" + $.query.remove('filter');
            window.location = "/opendata/search/" + newQuery;
        } 
        else {
            var newQuery = "" + $.query.set('filter', value);
            window.location = "/opendata/search/" + newQuery;
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
    },
    
    makeTabs: function(div) {
        $(div).tabs();
        }
  }    

