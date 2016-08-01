<html>

<head>

<title>
<?php
$cwd = explode("/",getcwd());
$folder = array_pop($cwd);
echo $folder;
?>
</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>

<style>

body {
    font-family: sans-serif;
}

.box {
float:left;
padding: 5px; /* space between image and border */
}

#images {
position:relative;
top: 30px;
}

/* dark theme */
/* body { */
/* background-color: black; */
/* color: white; */
/* } */

</style>

<script>


$(function() {

    // drag images and hover over others to overlay
    $( ".box" ).draggable({
        opacity: 0.35,
        helper: "clone",
        snap: true,
        revert: true,
    });

    // drag and drop to sort the images
    // $("#images").sortable();

    $( "input[id='filter']" ).on('keyup', function() {
        $("#message").html("");
        var pattern = $(this).val();
        var modifier = "";
        if(pattern.toLowerCase() == pattern) modifier = "i"; // like :set smartcase in vim (case-sensitive if there's an uppercase char)
        var elems = $(".box").filter(function() {
            var matches = this.id.match(new RegExp(pattern,modifier));  
            if(matches) {
                var legendTitle = $(this).find("fieldset > legend");
                legendTitle.html( "<b>"+legendTitle.text().replace(matches[0],"<font style='color:#F00'>"+matches[0]+"</font>")+"</b>" );
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
        }
    });
});

// vimlike: press / to focus on search box
$(document).keydown(function(e) {
    if(e.keyCode == 191) {
        console.log(e.keyCode); 
        e.preventDefault();
        $("#filter").focus().select();
    }
});

</script>

</head>

<body>


<input type="text" class="inputbar" id="filter" placeholder="Search/wildcard filter" />
<span id="message"></span>

<?php

$dirname = ".";

$files = scandir($dirname);

echo "<div id='images'>";
foreach($files as $curimg){

    if (!(strpos($curimg,'.png') || strpos($curimg,'.jpg'))) continue;

    /* $fname_no_ext = explode(".",$curimg); */
    /* $fname_no_ext = $fname_no_ext[0]; */
    $fname_no_ext = preg_replace('/\\.[^.\\s]{3,4}$/', '', $curimg);
    $fname_col_no_ext = $fname_no_ext;

    // find corresponding pdf and link to it if it exists
    $same_pdf = str_replace(".png", ".pdf", $curimg);
    $same_pdf = str_replace(".jpg", ".pdf", $same_pdf);
    $tolink = $curimg;
    if(in_array($same_pdf, $files)) $tolink = $same_pdf;

    $color="lightgray";

    $red="#B03A2E";
    $blue="#2874A6";
    $green="#32CD32";

    // why !== false? http://stackoverflow.com/questions/4366730/check-if-string-contains-specific-words
    // e vs mu
    if(strpos($curimg,"_el") !== false) {
        $color=$blue;
        $fname_col_no_ext = str_replace("_el", "<font style='color:$color'>_el</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_e_") !== false) {
        $color=$blue;
        $fname_col_no_ext = str_replace("_e_", "<font style='color:$color'>_e_</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_mu") !== false) {
        $color=$red;
        $fname_col_no_ext = str_replace("_mu", "<font style='color:$color'>_mu</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_m_") !== false) {
        $color=$red;
        $fname_col_no_ext = str_replace("_m_", "<font style='color:$color'>_m_</font>", $fname_col_no_ext);
    }

    // HH vs HL vs LL
    if(strpos($curimg,"HH") !== false) {
        $color=$red;
        $fname_col_no_ext = str_replace("HH", "<font style='color:$color'>HH</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"HL") !== false) {
        $color=$blue;
        $fname_col_no_ext = str_replace("HL", "<font style='color:$color'>HL</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"LL") !== false) {
        $color=$green;
        $fname_col_no_ext = str_replace("LL", "<font style='color:$color'>LL</font>", $fname_col_no_ext);
    }

    echo "
            <div class='box' id='$fname_no_ext'>
                <fieldset style='border:2px solid $color'>
                    <legend><b>$fname_col_no_ext</b></legend>
                    <a href='$tolink'>
                        <img src='$curimg' height='300px' />
                    </a>
                </fieldset>
            </div>
        ";
}
echo "\n";
echo "</div>";
echo "\n";
?>
</body>
</html>