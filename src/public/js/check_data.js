jQuery.ajaxSetup({ cache: false });

if (window.HW == undefined) {
    var HW = {};
}

HW.CheckData = HW.CheckData || {};


HW.CheckData.create = function() {
    var that = {},
        view = {},
        endpoint = {},
        api,
        context2d,
        canvas_width, canvas_height,
        model = {};
        
    
    that.setup = function(options) {
        view.canvas = $("#" + options.canvas);
        view.btnNG = $("#" + options.btnNG);
        view.btnOK = $("#" + options.btnOK);
        endpoint.server = options.serverUrl;
        // Init Options
        that.options = options;
        that.options.pw = options.pw || 5;
        // Register Events
        view.btnNG.click(function() {
            api.feedback(model.id, false, afterFeedback);
        });
        view.btnOK.click(function() {
            api.feedback(model.id, true, afterFeedback);
        })
        
        //
        api = HW.CheckData.API.create(endpoint);
        context2d = view.canvas[0].getContext("2d");
        canvas_width = view.canvas.width();
        canvas_height = view.canvas.height();
        return that;
    }
    
    var afterFeedback = function(response) {
        that.start();
    }
    
    that.start = function() {
        context2d.clearRect(0, 0, canvas_width, canvas_height);
        api.fetch(drawStrokes);
    }
    
    var drawStrokes = function(response) {
        model.id = response.id;
        var strokes = response.strokes;
        var char = response.char;
        // draw char
        context2d.lineWidth = 2;
        context2d.fillStyle = "black";
        context2d.font = "50px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'"
        context2d.fillText(char, 0, 50);
        // draw strokes
        context2d.lineWidth = that.options.pw/2;
        context2d.strokeStyle = "black";
//        context2d.beginPath();
//        $.each(strokes, function(i, stroke) {
//            context2d.beginPath();
//            context2d.moveTo(stroke[0][0], stroke[0][1]);
//            $.each(stroke.slice(1), function(j, p) {
//                context2d.lineTo(p[0], p[1]);
//            })
//            context2d.stroke();
//        });
//        context2d.stroke();
//        timerLoop(500, strokes, 0, drawing);
        drawing(strokes);
    }
    
    var timerLoop = function(wait, ary, index, loopFunc, finishFunc) {
        var item = ary[index];
        if (!item) {
            if (finishFunc) {finishFunc();}
            return;
        }
        loopFunc(index, item);
        setTimeout(function(){timerLoop(wait, ary, index+1, loopFunc, finishFunc)}, wait);
    }
    
    var drawing = function(strokes) {
        if (!strokes || strokes.length == 0) {
            return;
        }
        var stroke = strokes[0];
        context2d.beginPath();
        context2d.moveTo(stroke[0][0], stroke[0][1]);
        timerLoop(10, stroke, 1, function(j, p) {
            context2d.lineTo(p[0], p[1]);
            context2d.stroke();
        }, function() {
            setTimeout(drawing(strokes.slice(1)), 500);
        });
    }
    return that;
}

HW.CheckData.API = HW.CheckData.API || {};
HW.CheckData.API.create = function(endpoint) {
    var that = {};
    var endpoint = endpoint;
    that.feedback = function(data_id, is_ok, callback) {
        var params = {
                id: data_id,
                result: is_ok ? "ok" : "ng"
            };
        $.post(endpoint.server + "checked", params, function(response) {
            if (callback) {
                callback(response);
            }
        });
    }
    
    that.fetch = function(callback) {
        $.get(endpoint.server + "check_data", {p: Math.random()},  function(response) {
            callback(response);
        });
    }
    
    return that;
}

