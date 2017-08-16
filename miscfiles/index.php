<html>

<head>

<title>
<?php
$cwd = explode("/",getcwd());
$folder = array_pop($cwd);
echo $folder;
?>
</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />
<link rel="icon" type="image/png" href="../trashcan.png" />
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/jstree.min.js"></script>

<style>

#bintablecontainer {
    position: fixed;
    bottom: 0;
    width: 97%;
    padding: 10px; /* space between image and border */
}
#bintable {
    border: 1px solid black;
    background-color: rgba(250, 250, 250, .96);
    font-size: 8pt;
    font-family: monospace;
    padding: 10px; /* space between image and border */
}

body {
    font-family: sans-serif;
}

#custom-handle {
    width: 3em;
    font-family: sans-serif;
    /* height: 1.6em; */
    /* top: 50%; */
    /* margin-top: -.8em; */
    text-align: center;
    /* line-height: 1.6em; */
  }

#slider {
display:inline-block;
width: 200px;
top: 5px;
}


.box {
float:left;
padding: 5px; /* space between image and border */
border-radius: 5px;
}

/* /1* can remove if you don't want hover zoom *1/ */
/* .box:hover */
/* /1* if only hovering on the inner image is what matters, do .innerimg:hover *1/ */
/* { */
/*     box-shadow: 0px 0px 25px #555; */
/*     z-index: 2; */
/*     background-color: #fff; */
/*     -moz-transition:-moz-transform 0.5s ease-out; */ 
/*     -webkit-transition:-webkit-transform 0.5s ease-out; */ 
/*     -o-transition:-o-transform 0.5s ease-out; */
/*     transition:transform 0.5s ease-out; */
/*     -webkit-transition-delay: 1.0s; */
/*     -moz-transition-delay: 1.0s; */
/*     -o-transition-delay: 1.0s; */
/*     transition-delay: 1.0s; */
/*     transform: scale(2.3); */
/*     /1* transform: scale(1.0); *1/ */
/*     -moz-transform-origin: 0 0; */
/*     -webkit-transform-origin: 0 0; */
/*     -o-transform-origin: 0 0; */
/*     transform-origin: 0 0; */
/* } */

#images {
position:relative;
top: 30px;
}

legend {
font-weight: bold;
}

</style>

<?php

// get flat list with parent references
$data = array();
function fillArrayWithFileNodes( DirectoryIterator $dir , $theParent="#") {
    global $data;
    foreach ( $dir as $node ) {
        if (strpos($node->getFilename(), '.php') !== false) continue;
        if( $node->isDot() ) continue;
        if ( $node->isDir()) fillArrayWithFileNodes( new DirectoryIterator( $node->getPathname() ), $node->getPathname() );

        $tmp = array(
            "id" => $node->getPathname(),
            "parent" => $theParent,
            "text" => $node->getFilename(),
        );
        if ($node->isFile()) $tmp["icon"] = "file"; // can be path to icon file
        $data[] = $tmp;
    }
}
fillArrayWithFileNodes( new DirectoryIterator( '.' ) );

// get all files in flat list
$iter = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator('.', RecursiveDirectoryIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST,
    RecursiveIteratorIterator::CATCH_GET_CHILD
);
$paths = array('.');
foreach ($iter as $path => $dir) $paths[] = $path;

// get number of directories
$num_directories = 0;
foreach ( (new DirectoryIterator('.')) as $node ) {
    if( $node->isDot() ) continue;
    if ( $node->isDir()) $num_directories += 1;
}
?>

<script type="text/javascript">

function contains_any(str, substrings) {
    for (var i = 0; i != substrings.length; i++) {
       var substring = substrings[i];
       if (str.indexOf(substring) != - 1) {
         return substring;
       }
    }
    return null; 
}

function draw_objects(file_objects) {
    var jsrootbase = "http://uaf-8.t2.ucsd.edu/~namin/dump/jsroot/index.htm?json=../../.."+window.location.pathname;
    $("#images").html("");
    for (var ifo = 0; ifo < file_objects.length; ifo++) {
        var fo = file_objects[ifo];
        var name_noext = fo["name_noext"];
        var name = fo["name"];
        var path = fo["path"];
        var color = fo["color"];
        var pdf = fo["pdf"] || fo["name"];
        if (path) pdf = path+pdf;
        var txt_str = (fo["txt"].length > 0) ? " <a href='"+fo["txt"]+"' id='"+"text_"+fo["name_noext"]+"'>[text]</a>" : "";
        var extra_str = (fo["extra"].length > 0) ? " <a href='"+fo["extra"]+"' id='"+"extra_"+fo["name_noext"]+"'>[extra]</a>" : "";
        var json_str = (fo["json"].length > 0) ? " <a href='"+jsrootbase+fo["json"]+"' id='"+"json_"+fo["name_noext"]+"'>[js]</a>" : "";
        $("#images").append(
            "<div class='box' id='"+name_noext+"'>"+
                "    <fieldset style='border:2px solid "+color+"'>"+
                "        <legend>"+name_noext+txt_str+extra_str+json_str+"</legend>"+
                "        <a href='"+pdf+"'>"+
                "            <img class='innerimg' src='"+path+"/"+name+"' height='300px' />"+
                "        </a>"+
                "    </fieldset>"+
                "</div>"
        );
    }
}

function draw_filtered(filter_paths) {
        var temp_filelist = filelist.filter(function(value) {
            return contains_any(value, filter_paths);
        });

        var temp_objects = make_objects(temp_filelist);
        draw_objects(temp_objects);
}

function make_objects(filelist) {
    var file_objects = [];
    for (var i = 0; i < filelist.length; i++) {
        var f = filelist[i];
        var ext = f.split('.').pop();
        if (ext != "png") continue;
        var color = "";
        if (f.indexOf("HH") != -1) color = "#B03A2E";
        else if (f.indexOf("HL") != -1) color = "#2874A6";
        else if (f.indexOf("LL") != -1) color = "#32CD32";
        var name = f.split('/').reverse()[0];
        var path = f.replace(name, "");
        var name_noext = name.replace("."+ext,"");
        var pdf = (filelist.indexOf(path+name_noext + ".pdf") != -1) ? path+name_noext+".pdf" : "";
        var txt = (filelist.indexOf(path+name_noext + ".txt") != -1) ? name_noext+".txt" : "";
        var extra = (filelist.indexOf(path+name_noext + ".extra") != -1) ? name_noext+".extra" : "";
        var json = (filelist.indexOf(path+name_noext + ".json") != -1) ? name_noext+".json" : "";
        file_objects.push({
            "path": path,
            "name_noext": name_noext,
            "name":name,
            // "name":name+"?hash=<?php echo time(); ?>",
            "ext": ext,
            "pdf": pdf,
            "txt": txt,
            "extra": extra,
            "json": json,
            "color": color,
        });
    }
    return file_objects;
}

function register_hover() {
    console.log("registering hover");
    $("[id^=text_],[id^=extra_]").hover(
        function() {
            console.log("fading in hover");
            $(this).delay(1000).queue(function(){
                $(this).addClass('hovered').siblings().removeClass('hovered');
                var link = $(this).attr('href');
                console.log(link);
                $("#bintable").load(link, function() {
                    $("#bintable").html($("#bintable").html().replace(/\n/g,"<br>\n"));
                    $("#bintable").html($("#bintable").html().replace(/ /g,"&nbsp;"));
                    $("#bintable").html($("#bintable").html().replace("total_bkg","<b>total_bkg</b>"));
                });
                console.log("fading in");
                $("#bintable").fadeIn();
            });
        },function() {
            $(this).finish();
            $("#bintable").delay(500).fadeOut();
        } 
    );
}

// ultimately this will be a master filelist with all files recursively in this directory
// then we will filter for files we want to show
var obj = <?php echo json_encode($data); ?>;
var filelist = <?php echo json_encode($paths); ?>;


$(function() {

    if (<?php echo $num_directories?> > 0) {
        $('#jstree_demo_div')
            .on('changed.jstree', function(e,data) {
                draw_filtered(data.selected);
            })
            .jstree( {
                "core": {
                    'multiple': true,
                    'themes' : {
                       'stripes' : true
                    },
                    "data": 
                        obj
                    // test_data
                    // test_data2
                    
                }
            }); 
    }

    var handle = $( "#custom-handle" );
    $( "#slider" ).slider({
    value: 100,
        range: "min",
    min: 20,
    max: 250,
    create: function() {
        /* handle.text( $( this ).slider( "value" ) ); */
        handle.text( "100%" );
    },
        slide: function( event, ui ) {
            handle.text( ui.value + "%" );
            $("img").attr("height",300*ui.value/100);
        }
    });


        // filelist = filelist.filter(function(value) {
            // return value.indexOf("./plots/qcdEstimateData_2016_ICHEP_SNT/f_jets_mc/HT450to575_j2toInf_b0toInf") != -1;
        // });
        var file_objects = make_objects(filelist);
        draw_objects(file_objects);


    // drag images and hover over others to overlay

    /* $( ".box" ).draggable({ */
    /*     opacity: 0.50, */
    /*     helper: "clone", */
    /*     snap: true, */
    /*     revert: true, */
    /* }); */

    // make map from title of each plot to the html of the title
    var titleMap = {};
    var elems = $(".box").filter(function() {
        var legendTitle = $(this).find("fieldset > legend");
        titleMap[legendTitle.text()] = legendTitle.html();
    });

    $( "input[id='filter']" ).on('keyup', function() {
        $("#message").html("");
        var pattern = $(this).val();
        var modifier = "";
        if(pattern.toLowerCase() == pattern) modifier = "i"; // like :set smartcase in vim (case-sensitive if there's an uppercase char)
        var elems = $(".box").filter(function() {
            try {
            var regex = new RegExp(pattern,modifier);
            } catch(e) {
                return [];
            }
            var matches = this.id.match(regex);  
            if(matches) {
                var legendTitle = $(this).find("fieldset > legend");
                var to_replace =  titleMap[legendTitle.text()];
                to_replace = to_replace.replace(matches[0],"<font style='color:#F00'>"+matches[0]+"</font>") ;
                // console.log(to_replace);
                legendTitle.html(to_replace);
            }
            return matches;
        });
        if(pattern.length < 1) {
            $('.box').show();
            return;
        }
        $('.box').hide();
        if(elems.length == 0) {
            $("#message").html("No matching images!");
        } else {
            elems.show();
            register_hover();
        }
    });

    // if page was loaded with a parameter for search, then simulate a search
    // ex: http://uaf-6.t2.ucsd.edu/~namin/dump/plots_isfr_Aug26/?HH$
    if(window.location.href.indexOf("?") != -1) {
        var search = unescape(window.location.href.split("?")[1]);
        $("#filter").val(search);
        $("#filter").trigger("keyup");
    }

    register_hover();


});

// vimlike incsearch: press / to focus on search box
$(document).keydown(function(e) {
    if(e.keyCode == 191) {
        console.log(e.keyCode); 
        e.preventDefault();
        $("#filter").focus().select();
    }
});

function copyToClipboard(text) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}

function getQueryURL() {
    var query = escape($('#filter').val());
    var queryURL = "http://"+location.hostname+location.pathname+"?"+query;
    console.log(queryURL);
    copyToClipboard(queryURL)
}

</script>

</head>

<body>

  <div id="jstree_demo_div"> </div>

<input type="text" class="inputbar" id="filter" placeholder="Search/wildcard filter" />
<a href="javascript:;" onClick="getQueryURL();">copy as URL</a> &nbsp; &nbsp; 
<div id="slider"><div id="custom-handle" class="ui-slider-handle"></div></div>
<span id="message"></span>
<div id="images"></div>
<div id="bintablecontainer"  style="text-align: center;">
    <div id="bintable" style="display: inline-block; text-align: left; display: none">
    <!-- <div id="bintable" style="display: inline-block; text-align: left;"> -->
    </div>
</div>


</body>
</html>
