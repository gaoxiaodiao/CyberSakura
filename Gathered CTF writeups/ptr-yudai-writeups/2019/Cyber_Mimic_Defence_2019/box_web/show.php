<?php    
error_reporting(0);
session_start();
if(isset($_GET['reset'])){
        $_SESSION['id'] = null;
        header('location: show.php'); exit();
}
function checksql($id,$html){
	$_MIMICWEB[ 'db_server' ]   = '192.168.104.60';
	$_MIMICWEB[ 'db_database' ] = 'mimicweb_test';
	$_MIMICWEB[ 'db_user' ]     = 'injectTest01';
	$_MIMICWEB[ 'db_password' ] = 'VYW6LVhQWsj20ubn';
	$db = new PDO('mysql:host=' . $_MIMICWEB[ 'db_server' ].';dbname=' . $_MIMICWEB[ 'db_database' ].';charset=utf8', $_MIMICWEB[ 'db_user' ], $_MIMICWEB[ 'db_password' ]);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	if(is_numeric( $id )) {
		$data = $db->prepare( 'SELECT teamname, department FROM user WHERE id = (:id) LIMIT 1;' );
		$data->bindParam( ':id', $id, PDO::PARAM_INT );
		$data->execute();
		$row = $data->fetch();
		if( $data->rowCount() == 1 ) {
			$first = $row[ 'teamname' ];
			$last  = $row[ 'department' ];
			$html .= "<pre>ID: {$id}   战队: {$first}  单位/国家: {$last}</pre>";
		}
	}
	return $html;
}
    if(isset($_POST['id'])){
        $id = $_POST[ 'id' ];
		$html=checksql($id,'');
		$_SESSION['id']=$id;
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"><!---->
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <title>Easy WEB</title>
        <link href="/static/Press+Start+2P.css" rel="stylesheet">
        <link href="/static/nes.css" rel="stylesheet" />
        <link href="/static/style.css" rel="stylesheet" />
    </head>
    <body>
        <div class="container">
            <div class="main-container">
                <header>
                    <h1><a href="/" style="color: black;text-decoration:none;">Easy WEB</a></h1>
                    <p>Try hard to hack me.</p>
                    <section class="nes-container is-right with-title">
                        <h2 class="title">Main PAGE</h2>
                        <?php if(!$_SESSION['id']){ ?>
                        <form class="nes-field is-inline" action="show.php" method="POST">
                            <input name="id" type="text" id="inline_field" class="nes-input is-primary" placeholder="input your teamId">
                            <button type="submit" class="nes-btn is-primary">submit</button>
                        </form>
                        <?php }else{?>
                            <div class="nes-container with-title is-centered" style="margin-top:10px;">
                                <p class="title">This is your result</p>
                                <?php echo $html;?>
                            </div>
							<a href="/show.php?reset"><button type="button" class="nes-btn is-error">reset</button></a>
                        <? }?>
                    </section>
                </header>
            </div>
        </div>
    </body>
</html>
