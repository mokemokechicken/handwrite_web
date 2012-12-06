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
        infer_api,
        context2d,
        canvas_width, canvas_height,
        model = {};
        
    
    that.setup = function(options) {
        view.canvas = $("#" + options.canvas);
        view.btnNG = $("#" + options.btnNG);
        view.btnOK = $("#" + options.btnOK);
        view.btnInfer = $("#" + options.btnInfer);
        endpoint.server = options.serverUrl;
        // Init Options
        that.options = options;
        that.options.pw = options.pw || 5;
        // Initialize
        api = HW.CheckData.API.create(endpoint);
        context2d = view.canvas[0].getContext("2d");
        canvas_width = view.canvas.width();
        canvas_height = view.canvas.height();
        //
        infer_api = HW.repository.create(endpoint);
        // Register Events
        view.btnNG.click(function() {
            api.feedback(model.id, false, afterFeedback);
        });
        view.btnOK.click(function() {
            api.feedback(model.id, true, afterFeedback);
        })
        view.btnInfer.click(function() {
            infer_api.infer(model,{
                size: [canvas_width, canvas_height]
            }, showInferResult, false);
        });
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
        var strokes = response.strokes;
        var char = response.char;
        model.id = response.id;
        model.char = char;
        model.strokes = strokes;
        // draw char
        context2d.lineWidth = 2;
        context2d.fillStyle = "black";
        context2d.font = "50px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'"
        context2d.fillText(char, 0, 50);
        context2d.font = "15px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'"
        context2d.fillText("id="+model.id, 0, canvas_height-20);
        // draw strokes
        context2d.lineWidth = that.options.pw/2;
        context2d.strokeStyle = "black";
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
        timerLoop(3, stroke, 1, function(j, p) {
            context2d.lineTo(p[0], p[1]);
            context2d.stroke();
        }, function() {
            setTimeout(drawing(strokes.slice(1)), 400);
        });
    }
    
    var showInferResult = function(strokes, ys) {
        var predOrder = HW.Util.valueOrder(ys);
        for (var i=0; i<6; i++) {
            context2d.font = "50px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'"
            context2d.fillStyle = "black";
            context2d.fillText(that.options.chars[predOrder[i]], view.canvas.width()-70, 50 + i*50);
            context2d.font = "10px 'メイリオ', 'MS P明朝', 'ヒラギノ明朝 Pro'";
            context2d.fillStyle = "red";
            var p = Math.floor(ys[predOrder[i]] * 1000) / 10;
            context2d.fillText(p + "%" , view.canvas.width()-30, i*50+50);
        }
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

