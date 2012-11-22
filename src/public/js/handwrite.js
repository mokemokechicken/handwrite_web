jQuery.ajaxSetup({ cache: false });

var HW = {};

// Controller
HW.create = function() {
    var that = {};
    var context2d;
    var model;
    var repository;
    var view = {};
    var endpoint = {};
    
    that.setup = function(options) {
        view.canvas = $("#" + options.canvas);
        view.btnClear = $("#" + options.btnClear);
        view.btnSave = $("#" + options.btnSave);
        endpoint.server = options.serverUrl;
        // Init Options
        that.options = options;
        that.options.pw = options.pw || 5;
        that.options.chars = options.chars || "０１２３４５６７８９".split("");
        // Register EventHandler
        setupCanvas(view.canvas);
        view.btnClear.click(function() {
            that.start();
        });
        view.btnSave.click(function() {
            repository.addHWData(model,{
                size: [view.canvas.width(), view.canvas.height()]
            });
        });
        // Repository
        repository = HW.repository.create(endpoint);
        
        return that;
    }

    var setupCanvas = function(canvas) {
        canvas.bind("mousedown", function(e) {
            e.preventDefault();
            mousedown(e.offsetX, e.offsetY);
        })
        canvas.bind("touchstart", function(e) {
            e.preventDefault();
            var touch = e.originalEvent.changedTouches[0];
            var target = touch.target;
            mousedown(touch.pageX-target.offsetLeft, touch.pageY-target.offsetTop);
        })
        
        canvas.bind("mousemove", function(e){
            e.preventDefault();
            if (model.isDown) {
                mousemove(e.offsetX, e.offsetY);
            }
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
        context2d.lineJoin = "round";
        context2d.font = "50px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'"
        //context2d.font = "50px 'ヒラギノ明朝 Pro'"
    }
    
    that.start = function(info) {
        console.log("started");
        info = info || {};
        if (!info.char) {
            info.char = selectCharRandom();
        }
        model = HW.model.create();
        context2d.clearRect(0, 0, view.canvas.width(), view.canvas.height());
        context2d.lineWidth = 2;
        context2d.fillText(info.char, 0, 50);
        model.char = info.char;
        return that;
    }
    
    var selectCharRandom = function() {
        return that.options.chars[Math.floor(Math.random()*that.options.chars.length)];
    }
    
    var mousedown = function(x, y) {
        model.isDown = true;
        model.beginStroke(x,y);
    }
    
    var mousemove = function(x, y) {
        var lastPoint = model.lastPoint();
        model.addPoint(x,y);

        context2d.beginPath();
        context2d.lineWidth = that.options.pw;
        context2d.moveTo(lastPoint[0], lastPoint[1]);
        context2d.lineTo(x,y);
        context2d.stroke();
    }
    
    var mouseup = function() {
        model.isDown = false;
    }

    return that;
};

// Model
HW.model = {};
HW.model.create = function() {
    var that = {};
    that.isDown = false;
    that.strokes = [];
    that.char = null;
    
    that.beginStroke = function(x,y) {
        that.strokes.push([[x,y]]);
    }
    
    that.addPoint = function(x,y) {
        var currentStroke = that.strokes[that.strokes.length-1];
        currentStroke.push([x,y]);
    }
    
    that.lastPoint = function() {
        var currentStroke = that.strokes[that.strokes.length-1];
        return currentStroke[currentStroke.length-1];
    }
    
    return that;
}

// Repository
HW.repository = {};
HW.repository.create = function(endpoint) {
    var that = {};
    that.addHWData = function(model, meta) {
        var data;
        data = {
                meta: meta,
                char: model.char,
                strokes: model.strokes
        };
        var postString = JSON.stringify(data);
        console.log(postString);
        $.post(endpoint.server + "hwdata", postString, function(response) {
            console.log(response);
        });
    }
    return that;
}

