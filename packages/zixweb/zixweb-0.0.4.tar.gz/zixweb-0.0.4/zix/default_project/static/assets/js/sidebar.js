function isMobile() {
    var win = $(window);
    return (win.width() < 992);
}

function collapseSidebar() {
    let btn = $('.sidebar-toggle');
    let sidebar = $('.sidebar');    
    // btn.hide();
    sidebar.addClass('collapsed');
    // btn.fadeIn(100);
}

function expandSidebar() {
    let sidebar = $('.sidebar');    
    sidebar.removeClass('collapsed');
    sidebar.fadeIn(100);
}

function isSidebarCollapsed() {
    let sidebar = $('.sidebar');    
    return sidebar.hasClass('collapsed');
}

(function($) {
    let sidebarWidth = 150 + 20;
    let menuMarginRight = 30;
    let logoHolder = $('.logo-holder');
    let win = $(window);
    let w = win.width();
    let h = win.height();
    
    let body = $('body');
    let btn = $('.sidebar-toggle');
    let sidebar = $('.sidebar');
    let mainContent = $('.main-content');
    let topMenu = $('.top-menu');
    
    // Collapse on load    
    if (isMobile()) {
        collapseSidebar();
    }
    if (isSidebarCollapsed()) {
        topMenu.width(w - menuMarginRight);
        topMenu.css('margin-left', logoHolder.width());
    } else {
        topMenu.width(w - sidebarWidth - menuMarginRight); 
        topMenu.css('margin-left', sidebarWidth);        
    }    
    body.height(h);
    sidebar.height(h);
    mainContent.height(h);
    
    sidebar.removeClass('mobile-hid');
    
    // Events
    
    btn.click(toggleSidebar);
    
    function onResize() {
        if (w!=win.width()) {
            w = win.width();
        
            if (isMobile() && !isSidebarCollapsed()) {
                toggleSidebar();
                
            } else if (!isMobile() && isSidebarCollapsed()) {                
                toggleSidebar();
            }
            
            if (isSidebarCollapsed()) {
                topMenu.width(w - menuMarginRight);
                topMenu.css('margin-left', logoHolder.width());
 
            } else {
                topMenu.width(w - sidebarWidth - menuMarginRight); 
                topMenu.css('margin-left', sidebarWidth);
            }
        }
        if (h!=win.height()) {
            h = win.height();
            sidebar.height(h);
            mainContent.height(h);
            body.height(h);
        }
    }
    
    win.resize(function() {
        onResize();
    });
    
    onResize();
    
    function toggleSidebar() { 
        
        if (isMobile() || !isSidebarCollapsed()) {
            body.animate({'padding-left':'0'}, 100);
        }
        else if (!isMobile() && isSidebarCollapsed()) {
            body.animate({'padding-left':'14rem'},100);
        }
        
        if (!isSidebarCollapsed()) {
            sidebar.fadeOut(100,function(){
                collapseSidebar();
            });
        }
        else {
            expandSidebar();
        }
       
    }
})(jQuery)