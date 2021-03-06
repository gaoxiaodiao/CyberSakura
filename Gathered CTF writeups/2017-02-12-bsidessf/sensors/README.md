# Sensors (pwn)

###ENG
[PL](#pl-version)

In the tasks we get access to some web interface of scada-like application.
We quickly notice that in `robots.txt` there is `/firmware` so we proceed there and grab binaries for two pwn tasks.
For this task we focus on [sensor binary](sensor).
The binary has NX, Canary and Fortify so we assume there has to be a way to exploit this without doing any low-level magic.

In robots we can also see that there is `/flag.txt` but the webserver will not give it to us.

This binary sets up a CGI web interface and can be queried by http on the status of some sensors.
We can go to the URL `https://steel-mountain-d2fcf1e0.ctf.bsidessf.net/sensor?sensor=a-1` and this will show the status of `a-1` sensor.

We proceed with reversing the binary, which is statically compiled with come cgi-related library.
We focus on `main` function and `loadSensorConfig` function.
The latter is especially interesting because it opens a file and reads from it - a good target for reading the flag file:

```asm
00000000004015da         mov        r8d, 0x404192                               ; "sensors/%s.cfg", argument #5 for method j___snprintf_chk
00000000004015e0         mov        ecx, 0x80                                   ; argument #4 for method j___snprintf_chk
00000000004015e5         mov        edx, 0x1                                    ; argument #3 for method j___snprintf_chk
00000000004015ea         mov        esi, 0x80                                   ; argument #2 for method j___snprintf_chk
00000000004015ef         xor        eax, eax
00000000004015f1         call       j___snprintf_chk
00000000004015f6         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "s1" for method j_strcspn
00000000004015fb         mov        esi, 0x4044b4                               ; argument "s2" for method j_strcspn
0000000000401600         call       j_strcspn
0000000000401605         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "filename" for method j_fopen
000000000040160a         mov        esi, 0x4044cc                               ; argument "mode" for method j_fopen
000000000040160f         mov        byte [ss:rsp+rax+0x1a8+var_190], 0x0
0000000000401614         call       j_fopen
0000000000401619         test       rax, rax
000000000040161c         mov        rbx, rax
000000000040161f         jne        0x401641
;
0000000000401641         lea        rdi, qword [ss:rsp+0x1a8+var_110]           ; argument "str" for method j_fgets, XREF=loadSensorConfig+146
0000000000401649         mov        rdx, rax                                    ; argument "stream" for method j_fgets
000000000040164c         mov        esi, 0x100                                  ; argument "size" for method j_fgets
0000000000401651         call       j_fgets
0000000000401656         test       rax, rax
0000000000401659         mov        rdi, rbx
000000000040165c         jne        0x401665
```

We can also notice that if the loaded file is not a proper configuration of a sensor, it will call:

```asm
000000000040168c         mov        edi, 0x190                                  ; argument #1 for method cgiHeaderStatus
0000000000401691         call       cgiHeaderStatus
0000000000401696         lea        rsi, qword [ss:rsp+0x1a8+var_110]           ; argument #2 for method debug_printf
000000000040169e         mov        edi, 0x4041e8                               ; "Invalid configuration:\\n%s\\n", argument #1 for method debug_printf
00000000004016a3         xor        eax, eax
00000000004016a5         call       debug_printf
00000000004016aa         jmp        0x40163c
```

So it will actually print the contents of the file using `debug_printf`.
Looking at this function tells us that we simply need to set GET parameter `debug` to see the output of this function.

No we have to force the binary to read the flag file instead of the sensor file.
We can see that it calls `snprintf` with format `sensors/%s.cfg` with the input we provide.
If we could smuggle there a nullbyte we could cut the `.cfg` extension, and by using `../` we could go to the proper directory with the flag.
Unfortunately we can't do that because the input is already processed with `strcpy` with the cgi library, so any nullbytes are already removed at this point.
Our next thought was to provide long input, because `snprintf` will write only up to `n` characters, so if the input is long enough we could again end up with final string without `.cfg`.
But this doesn't work either because the cgi library is limiting the length of input parameter and it's always shorter than what we would need.
The `snprintf` has 0x80 bytes in buffer and the parameter is set in main to be at most 0x40 bytes.

But there is one curious thing in the code:

```asm
00000000004015f6         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "s1" for method j_strcspn
00000000004015fb         mov        esi, 0x4044b4                               ; argument "s2" for method j_strcspn
0000000000401600         call       j_strcspn
0000000000401605         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "filename" for method j_fopen
000000000040160a         mov        esi, 0x4044cc                               ; argument "mode" for method j_fopen
000000000040160f         mov        byte [ss:rsp+rax+0x1a8+var_190], 0x0
```

As we can see a function `strcspn` is called with our input as one parameter and some constant from `0x4044b4` as another one, and it actually sets 0x0 inside the string formed already by `snprintf` at index returned from `strcspn`! 
So in the end we can actually put a nullbyte there as long as `strcspn` returns index before the `.cfg`
If we look at the constant at `0x4044b4` we can see:

```asm
00000000004044b4         dd         '\x0d\x0a\x00w' 
```

So it seems passing `\r` or `\n` will trigger this.
This means that by passing as input `sensor=../flag.txt%0A` the `snprintf` will create `/sensors/../flag.txt\n.cfg` and then after `strcspn` this will change into `/sensors/../flag.txt\0.cfg` and therefore fopen will ignore `.cfg` opening the flag for us!

So finally running `https://steel-mountain-d2fcf1e0.ctf.bsidessf.net/sensor?sensor=../flag.txt%0A&debug` we get `flag:directory_traversal_in_c`

###PL version

W zadaniu dostajemy dost??p do webowego interfejsu aplikacji scada.
Szybko zauwa??amy ??e w `robots.txt` mamy informacje o katalogu `/firmware` z kt??rego wyci??gamy dwie binarki do zada?? pwn.
W tym zadaniu skupimy si?? na [aplikacji sensor](sensor).
Binarka ma NX, Canary i Fortify wi??c spodziewamy si??, ??e nale??y j?? exploitowa?? bez niskopoziomowej magii.

W robots widzimy te?? ??e jest `/flag.txt` ale serwer nie chce poda?? nam tego pliku.

Aplikacja wystawia za pomoc?? CGI interfejs webowy kt??ry pozwala po http odpytywa?? o stan sensor??w.
Mo??emy i???? pod url `https://steel-mountain-d2fcf1e0.ctf.bsidessf.net/sensor?sensor=a-1` i dostaniemy stan sensora `a-1`.

Nast??pnie przechodzimy do reversowania aplikacji, kt??ra jest statycznie kompilowana z jak???? bibliotek?? do cgi.
Skupiamy si?? na analizie funkcji `main` oraz `loadSensorConfig`.

Ta druga jest szczeg??lnie ciekawa bo otwiera plik i czyta z niego - mo??e da si?? za jej pomoc?? odczyta?? flag??:

```asm
00000000004015da         mov        r8d, 0x404192                               ; "sensors/%s.cfg", argument #5 for method j___snprintf_chk
00000000004015e0         mov        ecx, 0x80                                   ; argument #4 for method j___snprintf_chk
00000000004015e5         mov        edx, 0x1                                    ; argument #3 for method j___snprintf_chk
00000000004015ea         mov        esi, 0x80                                   ; argument #2 for method j___snprintf_chk
00000000004015ef         xor        eax, eax
00000000004015f1         call       j___snprintf_chk
00000000004015f6         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "s1" for method j_strcspn
00000000004015fb         mov        esi, 0x4044b4                               ; argument "s2" for method j_strcspn
0000000000401600         call       j_strcspn
0000000000401605         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "filename" for method j_fopen
000000000040160a         mov        esi, 0x4044cc                               ; argument "mode" for method j_fopen
000000000040160f         mov        byte [ss:rsp+rax+0x1a8+var_190], 0x0
0000000000401614         call       j_fopen
0000000000401619         test       rax, rax
000000000040161c         mov        rbx, rax
000000000040161f         jne        0x401641
;
0000000000401641         lea        rdi, qword [ss:rsp+0x1a8+var_110]           ; argument "str" for method j_fgets, XREF=loadSensorConfig+146
0000000000401649         mov        rdx, rax                                    ; argument "stream" for method j_fgets
000000000040164c         mov        esi, 0x100                                  ; argument "size" for method j_fgets
0000000000401651         call       j_fgets
0000000000401656         test       rax, rax
0000000000401659         mov        rdi, rbx
000000000040165c         jne        0x401665
```

Mo??emy zauwa??y?? te??, ze je??li wczytany plik nie jest poprawn?? konfiguracj?? dla sensor??w to wykonane zostanie:

```asm
000000000040168c         mov        edi, 0x190                                  ; argument #1 for method cgiHeaderStatus
0000000000401691         call       cgiHeaderStatus
0000000000401696         lea        rsi, qword [ss:rsp+0x1a8+var_110]           ; argument #2 for method debug_printf
000000000040169e         mov        edi, 0x4041e8                               ; "Invalid configuration:\\n%s\\n", argument #1 for method debug_printf
00000000004016a3         xor        eax, eax
00000000004016a5         call       debug_printf
00000000004016aa         jmp        0x40163c
```

Wi??c ta funkcja wypisze nam zawarto???? niepoprwanego pliku za pomoc?? `debug_printf`.
Analiza tej funkcji pozwala stwierdzi?? ??e wystarczy ustawi?? parametr GET `debug` ??eby widzie?? jej wyniki.

Teraz pozostaje nam zmusi?? binarke do wczytania flagi zamiast konfiguracji sensora.
Widzimy ??e wywo??ywane jest `snprintf` z formatem `sensors/%s.cfg` dla danych kt??re wprowadzimy.
Gydyby??my mogli przemyci?? tam nullbyte to ko??c??wka `.cfg` zosta??aby uci??ta i za pomoc?? `../` mogliby??my wyj???? do katalogu z flag?? i j?? odczyta??.
Niestety nie mo??emy tego zrobi?? bo dane s?? ju?? wcze??nie przetworzone przez `strcpy` w bibliotece cgi i wszystkie nullbyte s?? usuni??te kiedy tu dochodzimy.
Nasza kolejna my??l to wprowadzenie d??ugiego inputu, poniewa?? `snprintf` zapisze nie wi??cej ni?? `n` znak??w, wi??c gdyby input by?? odpowiednio d??ugi mogliby??my zn??w uzyska?? wynikowy string bez `.cfg`.
Niestety to te?? nie jest mo??liwe bo biblioteka cgi limituje d??ugo???? parametru i zawsze jest za kr??tki.
Funkcja `snprintf` ma bufor na 0x80 znak??w a parametry s?? w main ograniczane do 0x40 bajt??w.

Ale w kodzie jest pewna ciekawa rzecz:

```asm
00000000004015f6         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "s1" for method j_strcspn
00000000004015fb         mov        esi, 0x4044b4                               ; argument "s2" for method j_strcspn
0000000000401600         call       j_strcspn
0000000000401605         lea        rdi, qword [ss:rsp+0x1a8+var_190]           ; argument "filename" for method j_fopen
000000000040160a         mov        esi, 0x4044cc                               ; argument "mode" for method j_fopen
000000000040160f         mov        byte [ss:rsp+rax+0x1a8+var_190], 0x0
```

Jak wida?? funkcja `strcspn` jest wywo??ywana z naszym wej??ciem i jak???? sta???? z `0x4044b4` jako drugim parametrem i nast??pnie bajt 0x0 jest ustawiany wewn??trz stringa przygotowanego ju?? przez `snprintf` a takim indeksie jaki zwr??ci `strcspn`!
Wi??c mo??emy ustawi?? nullbyte o ile `strcspn` zr??ci indeks przed `.cfg`
Je??li zerkniemy teraz na sta???? pod `0x4044b4` zobaczymy:

```asm
00000000004044b4         dd         '\x0d\x0a\x00w' 
```

Z czego wynika ze wys??anie `\r` lub `\n` da oczekiwany przez nas efekt dodania nullbyte.
To oznacza ??e dla wej??cia `sensor=../flag.txt%0A` `snprintf` utworzy ??cie??k?? `/sensors/../flag.txt\n.cfg` a nast??pnie po `strcspn` to zostanie zmienione na `/sensors/../flag.txt\0.cfg` a tym samym fopen zignoruje `.cfg` i otworzy dla nas flag??!

Finalnie uruchomienie `https://steel-mountain-d2fcf1e0.ctf.bsidessf.net/sensor?sensor=../flag.txt%0A&debug` daje nam `flag:directory_traversal_in_c`
