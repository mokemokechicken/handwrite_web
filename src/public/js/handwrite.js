var HW = {};

HW.create = function() {
    var that = {};
    var context2d;
    
    that.setup = function(options) {
        that.options = options;
        that.options.pw = options.pw || 5;
        return that;
    }

    that.start = function() {
        console.log("started");
        var canvas = $("#" + that.options.canvas);
        
        canvas.bind("mousedown", function(e) {
            e.preventDefault();
            mousedown(e.offsetX, e.offsetY);
        })
        canvas.bind("touchstart", function(e) {
            e.preventDefault();
            var touch = e.originalEvent.changedTouches[0];
            var target = touch.target;
            console.log(touch);
            mousedown(touch.pageX-target.offsetLeft, touch.pageY-target.offsetTop);
        })
        
        canvas.bind("mousemove", function(e){
            e.preventDefault();
            mousemove(e.offsetX, e.offsetY);
        });
        canvas.bind("touchmove", function(e) {
            e.preventDefault();
            var touch = e.originalEvent.changedTouches[0];
            var target = touch.target;
            mousemove(touch.pageX-target.offsetLeft, touch.pageY-target.offsetTop);
        })
        
        canvas.bind("mouseup", function(e) {
            mouseup();
        })
        canvas.bind("touchend", function(e) {
            mouseup();
        })
        
        context2d = canvas[0].getContext("2d");
        return that;
    }
    
    var mousedown = function(x, y) {
        context2d.beginPath();
        context2d.arc(x, y, that.options.pw, 0, Math.PI*2, false);
        context2d.fill();
    }
    
    var mousemove = function(x, y) {
        context2d.beginPath();
        context2d.arc(x, y, that.options.pw, 0, Math.PI*2, false);
        context2d.fill();
    }
    
    var mouseup = function() {
    }
    
    return that;
};




