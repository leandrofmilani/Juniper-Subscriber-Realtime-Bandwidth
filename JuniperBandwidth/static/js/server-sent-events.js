if(typeof(EventSource) !== "undefined") {

    var up = 0;
    var down = 0;
    var time = new Date();
    var pause = false;
    var showData = true;
    var cnt = 0;

    var source = new EventSource("/data");
    source.onmessage = function(event) {
        var data = JSON.parse(event.data);
        document.getElementById("loading").style.display = 'none';

        if (data['error']){
            var msg = data['error'];
            source.close();
            document.getElementById("alert").style.display = 'block';
            document.getElementById("alert").innerHTML = msg;
        }else{
            if (showData){
                var username = data["username"];
                var filterin = data["filterin"];
                var filterout = data["filterout"];
                var ipaddress = data["ipaddress"];
                document.getElementById("pppoe").innerHTML = username;
                document.getElementById("ipaddress").innerHTML = ipaddress;
                document.getElementById("filterin").innerHTML = filterin;
                document.getElementById("filterout").innerHTML = filterout;
                document.getElementById("info").style.display = 'block';
                Plotly.plot('chart', toPlot, layout,{responsive: true, displayModeBar: false});
                showData = false;
            }
            up = data["up"];
            down = data["down"];
            document.getElementById("download").innerHTML = getSpeed(down);
            document.getElementById("upload").innerHTML = getSpeed(up);
            updateChart();
        }						
    }

    function roundToTwo(num) {    
        return +(Math.round(num + "e+2")  + "e-2");
    }

    function getSpeed(speed) {
        if (speed >= 1024){
            var value_mbps = (speed / 1024);
            var mbps = roundToTwo(value_mbps);
            var data = `${mbps} Mbps`;
            return data;
        }else{
            var data = `${speed} Kbps`;
            return data;
        }
    }

    function pause_continue(){
        var currentvalue = document.getElementById('pause_continue').value;
        if(currentvalue == 'Continue'){
            document.getElementById('pause_continue').value='Pause';
            pause = false;
        }else{
            document.getElementById('pause_continue').value='Continue';
            pause = true;
        }
    }
    
    var upload = {
        x: [time],
        y: [up],
        hovertemplate: '%{y} kbps',
        name: "Upload",
        mode: 'line'
    };

    var download = {
        x: [time],
        y: [down],
        hovertemplate: '%{y} kbps',
        line: {
            color: 'rgb(255,0,0)'
        },
        name: "Download",
        mode: 'line'
    };

    var toPlot = [upload,download];

    var layout = {
        showlegend: false,
        plot_bgcolor: '#303030',
        paper_bgcolor: '#333',
        gridcolor: '#fff',
        margin: {
            l: 50,
            r: 50,
            t: 5,
            b: 25,
        },
        xaxis: {
            tickformat: '%H:%M:%S',
            tickfont: {color: '#fff'}
        },
        yaxis: {
            title: 'Kbps',
            rangemode: 'tozero',
            titlefont: {color: '#fff'},
            tickfont: {color: '#fff'}
        }
    };
    
    function updateChart() {
        var time = new Date();
        Plotly.extendTraces('chart', {
            x: [[time], [time]],
            y: [[up], [down]]
        }, [0, 1])
        cnt++;
        if(cnt >= 30 && pause == false) {
            document.getElementById("pause").style.display = 'block';
            Plotly.relayout('chart',{
                xaxis: {
                    range: [time.getTime()-(60*1000),time.getTime()+(2*1000)],
                    tickformat: '%H:%M:%S',
                    tickfont: {color: '#fff'}
                }
            });
        }
    }

}else{
    alert('Sorry! No server-sent events support in this browser...');
}