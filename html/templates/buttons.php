<?php
if ($_GET['run']) {
    exec("../scripts/nas-control.sh");
    echo "Worked!";
};

if ($_GET['start_nas']) {
    exec("../scripts/wake-up.sh");
}
?>