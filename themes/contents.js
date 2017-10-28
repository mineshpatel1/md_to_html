function loadFunc() {
    var toggled = false;

    // Build Navbar
    $(".navbar").append(
        $("<h2>Contents</h2>").append(
            $("<span class='collapse toggleAll'>-</span>").click(function() {
                toggleAll(this);
            })
        )
    );
    $(".navbar").append("<div class='search'><span>Search</span><input></input></div>");
    $(".navbar").append($("#TOC"));
    $(".canvas, #header").click(function() {
        if (toggled) {
            $(".navbar").animate({width: "0px"}, "fast");
            $(".header_banner").animate({left: "0"}, "fast");
            $(".canvas").animate({left: "0px"}, "fast");
            $("#header").animate({left: "0px"}, "fast");
            $(".content_button").animate({left: "0px"}, "fast");
            $(".chevron").text(">");
            toggled=false;
        }
    });

    // Enable content animations
    $(".content_button").click(function() {
        if(toggled) {
            $(".navbar").animate({width: "0px"}, "fast");
            $(".header_banner").animate({left: "0"}, "fast");
            $(".canvas").animate({left: "0px"}, "fast");
            $("#header").animate({left: "0px"}, "fast");
            $(".content_button").animate({left: "0px"}, "fast");
            $(".chevron").text(">");
            toggled=false;
        } else {
            $(".navbar").animate({width: "336px"}, "fast");
            $(".header_banner").animate({left: "336"}, "fast");
            $(".canvas").animate({left: "336px"}, "fast");
            $(".content_button").animate({left: "336px"}, "fast");
            $("#header").animate({left: "336px"}, "fast");
            $(".chevron").text("<");
            toggled=true;
        }
    });

    $(".navbar").find("a").each(function() {
        var list = $(this).next();
        if (list.length > 0) {
            $(this).before("<span class='toggleList collapse'>-</span>");
            $(this).prev().click(function() {
                if ($(this).hasClass("collapse")) {
                    $(this).text("+").removeClass("collapse");
                } else {
                    $(this).text("-").addClass("collapse");
                }
                list.animate({height: 'toggle'});
            });
        } else {
            $(this).before("<span class='hiddenToggle'>-</span>");
        }
    });

    // # Implement Search Bar
    $(".navbar .search input").keyup(function() {
        expandAll();
        var val = $(this).val().toLowerCase();
        $(".navbar a").each(function() {
            var link = $(this).text().toLowerCase();
            if (link.indexOf(val) >= 0) {
                $(this).show(); $(this).prev().show();
            } else {
                $(this).hide(); $(this).prev().hide();
            }
        });
    });

    // Expand/Collapse All functionality
    function toggleAll(el) {
        if ($(el).hasClass('collapse')) {
            $(el).removeClass('collapse');
            $(el).text('+');
            collapseAll();
        } else {
            $(el).addClass('collapse');
            $(el).text('-');
            expandAll();
        }
    }

    function collapseAll() {
        $("ul>li>.toggleList").text('+').removeClass('collapse').nextUntil("ul").next().animate({height: 'hide'});
    }

    function expandAll() {
        $("ul>li>.toggleList").text('-').addClass('collapse').nextUntil("ul").next().animate({height: 'show'});
    }