<html>

<head>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

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

</style>

<script>


$(function() {
    $( "input[id='filter']" ).on('keyup', function() {
        $("#message").html("");
        var needle = $(this).val();
        needle = needle.replace(/\*/g, "")
            if(needle.length < 1) {
                $('.box').show();
                return;
            }
        console.log( $(this).val() );
        $('.box').hide();
        var elems = $('[id*='+needle+']');
        if(elems.length == 0) {
            console.log("no matching names"); 
            $("#message").html("No matching images!");
        } else {
            elems.show();
        }
    });
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

    $fname_no_ext = explode(".",$curimg);
    $fname_no_ext = $fname_no_ext[0];
    $fname_col_no_ext = $fname_no_ext;

    // find corresponding pdf and link to it if it exists
    $same_pdf = str_replace(".png", ".pdf", $curimg);
    $same_pdf = str_replace(".jpg", ".pdf", $same_pdf);
    $tolink = $curimg;
    if(in_array($same_pdf, $files)) $tolink = $same_pdf;

    /* $color="#21618C"; */
    $color="lightgray";
    if(strpos($curimg,"_el")) {
        $color="#2874A6";
        $fname_col_no_ext = str_replace("_el", "<font style='color:$color'>_el</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_e_")) {
        $color="#2874A6";
        $fname_col_no_ext = str_replace("_e_", "<font style='color:$color'>_e_</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_mu")) {
        $color="#B03A2E";
        $fname_col_no_ext = str_replace("_mu", "<font style='color:$color'>_mu</font>", $fname_col_no_ext);
    }
    if(strpos($curimg,"_m_")) {
        $color="#B03A2E";
        $fname_col_no_ext = str_replace("_m_", "<font style='color:$color'>_m_</font>", $fname_col_no_ext);
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
