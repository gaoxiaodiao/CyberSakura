<?php
/**
 * This is not a web challenge!
 * Your target is only the binary executed by PHP.
 */
require 'recaptcha.php'; // for reCAPTCHA

function h($text) {
    return htmlspecialchars($text,
                            ENT_COMPAT | ENT_HTML401 | ENT_SUBSTITUTE,
                            'UTF-8');
}

function close_all($proc, $pipes) {
    foreach($pipes as &$pipe) {
        if ($pipe) fclose($pipe);
    }
    unset($pipes);
    return proc_close($proc);
}

function rot13($input, $timeout_sec = 15) {
    $timeout = time() + $timeout_sec;

    // Open process
    $desc = array(
        0 => array('pipe', 'r'),
        1 => array('pipe', 'w'),
        2 => array('pipe', 'w'),
    );
    $pipes = NULL;
    $proc = proc_open('./rot13', $desc, $pipes, getcwd(), NULL);
    if (!is_resource($proc)) {
        return '<ERROR> Could not open process';
    }
    stream_set_blocking($pipes[0], 0);
    stream_set_blocking($pipes[1], 0);
    stream_set_blocking($pipes[2], 0);

    // Send input
    fwrite($pipes[0], $input);

    $output = '';
    while(true) {
        // Receive output
        foreach(array(1, 2) as $fd) {
            do {
                $data = fread($pipes[$fd], 4096);
                $output .= $data;
            } while(strlen($data) > 0);
        }

        // Check status
        $status = proc_get_status($proc);
        if ($status === FALSE) {
            close_all($proc, $pipes);
            return '<ERROR> Could not get process status';
        }
        if ($timeout - time() <= 0) {
            close_all($proc, $pipes);
            return '<ERROR> Timeout';
        }
        if ($status['running'] === FALSE) {
            return $output;
        }
    }
}

if (!empty($_GET['input'])) {
    $input = (string)$_GET['input'];
    if (reCAPTCHA()) {
        $output = rot13($input);
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>ROT13</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <script src="https://www.google.com/recaptcha/api.js"></script>
    </head>
    <body>
        <div class="container">
            <h1 class="mt-3">ROT13 Converter</h1>
            <form action="/" method="GET">
                <fieldset>
                    <div class="form-group">
                        <label for="input">Input:</label>
                        <input type="text" class="form-control" name="input" id="input" placeholder="NOP13" value="<?php if (isset($input)) { print(h($input)); } ?>">
                    </div>
                    <div class="form-group">
        	              <div class="g-recaptcha" data-sitekey="6LcZ1r0UAAAAAJcyneDQonYeGx_ulXuSXpKRux_R"></div>
                    </div>
                    <button type="submit" class="btn btn-primary">Convert!</button>
                </fieldset>
            </form>
            <?php if (isset($output)) { ?>
                <hr>
                <div class="form-group">
                    <label for="output">Output:</label>
                    <input type="text" class="form-control" name="output" id="output" value="<?php print(h($output)); ?>" readonly>
                </div>
            <?php } ?>
        </div>
    </body>
</html>
