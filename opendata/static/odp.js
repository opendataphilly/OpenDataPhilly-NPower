var odp = {
    tags: null,

    setupSearchInput: function () {
        if ($.query.get('qs') && $.query.get('qs') != "") {
            $("#qs")[0].value = decodeURI($.query.get('qs')).replace(/\x2B/g, " ");
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
            evt.stopImmediatePropagation();
            evt.preventDefault();
            if ($("#qs")[0].value != "" && $("#qs")[0].value != "Search for data") {
                window.location = "/opendata/search/?sort=name&dir=asc&qs=" + decodeURI($("#qs")[0].value); 
            } else {
                window.location = "/opendata/search/?sort=name&dir=asc";
            }
        });
        
        $("#search_img").click(function(evt) {
            $("#search_form").submit();
        });
        
    },
    
    setupNominate: function() {
        $("#form_container").hide();
        $("#nominate_button").click(function() {
            $("#form_container").show()
            $("#nominate_button").hide()
        });
        
        if ($.query.get('nqs') && $.query.get('nqs') != "") {
            $("#nqs")[0].value = decodeURI($.query.get('nqs')).replace(/\x2B/g, " ");
        }

        $("#nqs").focus(function (evt) {
            if (this.value == "Search for nominations") {
                this.value = "";
            }
        });
        $("#nqs").focusout(function (evt) {
            if(this.value == "") {
                this.value = "Search for nominations";
            }
        });
        
        $("#n_search_form").submit(function(evt) {
            evt.stopImmediatePropagation();
            evt.preventDefault();
            if ($("#nqs")[0].value != "" && $("#nqs")[0].value != "Search for nominations") {
                window.location = "/opendata/nominate/?nqs=" + decodeURI($("#nqs")[0].value); 
            } else {
                window.location = "/opendata/nominate/";
            }
        });

        $("#n_search_img").click(function(evt) {
            $("#n_search_form").submit();
        });
        
        odp.setupNomFilterLinks();
        odp.setupNomSortLinks();
        
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
    
    setupNomSortLinks: function () {
        var sort_name = $("#sort_suggested_date > a").addClass("url_image")[0];
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
    
    setupNomFilterLinks: function () {
        var filter_mine = $("#filter_mine > a").addClass("url_image")[0];
        filter_mine.innerHTML = '';
        
        if ($.query.get('filter')) {
            st = $.query.get('filter');
            $("#filter_" + st + " > a")[0].style.backgroundPosition="0 -40px";
        }
        $("#filter .url_image").hover(function() {
            this.style.backgroundPosition="0 -81px";
        }, function () {
            var filter_split = this.parentNode.id.split('filter_');
            if ($.query.get('filter') && $.query.get('filter') == filter_split[1]) {
                this.style.backgroundPosition="0 -40px";
            } else {
                this.style.backgroundPosition="0 0";
            }
        });
    },
    
    getFiltered: function (value) {
        
        if ($.query.get('filter') == value) {
            var newQuery = "" + $.query.remove('filter');
            window.location = window.location.pathname + newQuery;
        } 
        else {
            var newQuery = "" + $.query.set('filter', value);
            window.location = window.location.pathname + newQuery;
        }
    },
    getNomFiltered: function () {
        if ($.query.get('filter') == 'mine') {
            var newQuery = "" + $.query.remove('filter');
            window.location = window.location.pathname + newQuery;
        } 
        else {
            var newQuery = "" + $.query.set('filter', 'mine').set('sort', 'suggested_date').set('dir', 'desc');
            window.location = window.location.pathname + newQuery;
        }
    },
    setupCommentForm: function () {
        $('#resource_comment_form').submit(function (evt) {
            if ($("#id_comment")[0].value == "" || !$("#id_rating_0").hasClass("star-rating-on")) {
                evt.stopImmediatePropagation();
                evt.preventDefault();
                $('#comment_field_errors')[0].innerHTML = "You must enter both a comment and select a rating."
            }
        });
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
            tag_list += "<li id='" + tag.pk + "'><a class='tag' href='/opendata/tag/" + tag.pk + "/?sort=name&dir=asc'>" + tag.fields.tag_name + "</a></li>"
        }
        $("#tag_list").replaceWith(tag_list);
        
        odp.setNavLink();
    },
    
    makeTabs: function(div) {
      $(div).each(function () {
        $(this).tabs();
      });
    },
    
    setDialogImage: function(source) {        

    },
    
    makeDialog: function(div) {
        $(div).each(function () {
            //make the dialog for each thumb
            var $dialog = $(this).find('.dialog');
            $dialog.dialog({
              autoOpen: false,
              modal: true,
              draggable: false,
              width: 'auto'
            });
            //open dialog by clicking the thumb
            $(this).click(function() {
              $dialog.dialog("open");
              return false;
           });
           // close the window when clicking the overlay background
           $('.ui-widget-overlay').live("click", function() {
              $dialog.dialog("close");
          });   
         });
      },
    
    setNavLink: function() {
        var loc = window.location.href;
        if(loc.indexOf("/tag/") != -1) {
            var id = loc.split("/tag/")[1].split("/")[0];
            $("#" + id).addClass('active_page');
        } else {
            loc = loc.split("/");
            for(var i = 0; i < loc.length; i++) {
                var val = loc.pop();
                if (val != "" && val.indexOf("=") == -1) {
                    var test = $("#" + val);
                    if (test.length == 1) {
                        test.addClass('active_page');
                        return;
                    }
                }
            }            
        }
    }
}
      

