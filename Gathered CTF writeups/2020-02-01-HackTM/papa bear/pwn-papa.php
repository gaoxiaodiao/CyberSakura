<?php
const TARGET = "WWWWWMWWWWWMWMMMWWWWWWWWWMMMWMWWWWMWWWMMWMMMWWWWWMMMMMMWMMMWWWMMMMWWMWWMWWMMMMMMWWWWMMWWWMWWWWWWMMWWWWMWMWMMMWWWWMMMMMWMWMMMWMMWWWMWMMMMMMMMWMMMMWWWMMWWMWMWMMWWMWWWWMWWMMWMMWWWWWWWWMMWWWWWWWMMWWWWMMWWWWMWMMMMWWWWWMMWWMWWWWWWMWMWWWMMWWMWMWWWWMWWWWMWWMMMWMWMWWWWMMMMWWMMMMMMMMM";

function score($string)
{
    for($i = 0; $i < strlen(TARGET); $i++)
        if(TARGET[$i] !== $string[$i])
            break;

    return $i;
}

function check($password)
{
    $cmd = sprintf("./papa_bear %s 0>&1", escapeshellarg($password));
    $p   = popen($cmd, "r");

    /* Discard papa bear */
    for($i = 0; $i < 7; $i++)
        fgets($p);

    /* Read MW */
    $buffer = "";
    for($i = 0; $i < 7; $i++)
        $buffer .= fgets($p);

    fclose($p);

    /* Remove unwanted characters */
    $clear  = "pbdqPQ-= \n";
    $buffer =  str_replace(str_split($clear), "", $buffer);
    echo $buffer; 
    // assert(275 === strlen($buffer));
    return $buffer;
}

$charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_/+";
$flag    = ""; //"HackTM{F4th3r bEaR s@y$: Smb0DY Ea7 My Sb3VE}";

while(false === strpos($flag, "}")) {
    $score = 0;
    $best  = [];

    //for($i = 0; $i < strlen($charset); $i++) {
    for($i = 0x20; $i < 0x7F; $i++) {
        $char = chr($i);
        //$char = $charset[$i];
        $c = check($flag . $char);
        $s = score($c);

        if($s == $score) {
            $best[] = $char;
        } else if($s > $score) {
            $score = $s;
            $best  = [$char];
        }
    //  printf("%d %s %d\n", $i, $charset[$i], score($c));
    }

    if(sizeof($best) !== 1) {
        var_dump($best);
        throw new Exception("too much");
    }

    $flag .= $best[0];
    printf("%s\n", $flag);
}