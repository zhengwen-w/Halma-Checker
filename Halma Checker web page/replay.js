function makePeg(x, y, color) {
    var peg = $('<img class="peg">');
    peg.addClass('col_' + x);
    peg.addClass('row_' + y);
    peg.attr('id', 'peg_' + x + '_' + y);
    peg.attr('src', 'img/' + color + '.png');
    return peg;
}

function getTile(x, y) {
    return $('#tile_' + x + '_' + y);
}

function getPeg(x, y) {
    return $('#peg_' + x + '_' + y);
}

var t2 = 40;

function replay(file) {
    t2 = parseInt($('#timeIntervalInput').val(), 10);
    var fileReader = new FileReader();
    fileReader.onload = function(fileLoadedEvent){
        var data = fileLoadedEvent.target.result;
        var lines = data.split('\n');
        var line;
        var tokens;
        var i;

        // Initialize the configuration
        pegContainer.empty();
        for (i = 0; i < 16; ++i) {
            line = lines[i].trim();
            var j;
            for(j = 0; j < 16; ++j){
                var c = line[j];
                if(c !== '.'){
                    pegContainer.append(makePeg(j, i, c === 'W'?'white':'black'));
                }
            }
        }

        var turn;
        var player;
        var from;
        var to;

        function recur1(){
            ++i;  // pass the empty line
            line = lines[i];
            if(!line)
                return;

            tokens = line.split(' ');
            turn = tokens[0];
            player = tokens[1];
            turnInfo.text(turn);
            playerInfo.text(player);

            ++i;
            line = lines[i];
            tokens = line.split(' ');
            from = tokens[1].split(',');
            getTile(from[0], from[1]).addClass('active');

            function recur2(){
                setTimeout(function(){
                    line = lines[i];
                    if(!line){
                        $('.active').removeClass('active');
                        recur1();
                        return;
                    }
                    tokens = line.split(' ');
                    from = tokens[1].split(',');
                    to = tokens[2].split(',');
                    getPeg(from[0], from[1]).remove();
                    getTile(to[0], to[1]).addClass('active');
                    pegContainer.append(makePeg(to[0], to[1], player.toLowerCase()));
                    ++i;
                    recur2();
                }, t2);
            }

            recur2();
        }

        recur1();
    };
    fileReader.readAsText(file, "UTF-8");


    var pegContainer = $('#pegsDiv');
    var turnInfo = $('#turnInfo');
    var playerInfo = $('#playerInfo');
}

function initPage() {
    $('#replayBtn').click(function(){
        var file = $('#fileInput')[0].files[0];
        replay(file);
    })
}