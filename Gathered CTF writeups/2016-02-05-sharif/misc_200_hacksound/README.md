## Hack By The Sound (Misc, 200p)

    A well known blogger has came to a hotel that we had good relationships with its staffs. We tried to capture the sound of his room by placing a microphone inside the desk.

    We have recorded the sound about the time that he has typed a text in his blogg. You could find the text he typed in "Blog Text.txt".
    
    We reduce noises somehow and found that many characters may have the same keysound. Also we know that he use meaningful username and password.
    
    Could you extract the username and password of his blog?
    
    flag is concatenation of his username and password as usernamepassword.
    
    Download sound.tar.gz

###ENG
[PL](#pl-version)

The attached .wav file had no sound loud enough for our ears, but amplifying it using Audacity we were able to notice
that it was sound of a person typing. Words were pretty noticeable - space always meant that typing stops for a split
second. By ear, all the key sounds were identical though.

However, we checked out Audacity's wave representation of keys and overlaid some of them in GIMP. Here is the result:
![](http://i.imgur.com/royrw1X.png)

The first image is two "S" sounds overlaid - there were almost no changes. The second one - "O" and "I" - had minor
differences, and the last one - "N" and "A" - showed noticeable changes. Apparently, the further the keys are on the
keyboard, the more differences they have. 

The task now was obvious, but still hard. In the end, we did the following:
- read raw data from the wav
- found the sound peaks, corresponding to individual key presses
- cut about 0.05s worth of sound around each peak
- repair blog text - there were some extra characters in a couple of places, which made keysound-to-character
  correspondence wrong
- for each unknown keypress, iterate over known keypresses and try to find best fit

Unfortunately, some characters had the same sound, so we were unable to find the password in plaintext - instead, we
got a range of characters for each position:

```
[] [] [ced] [frv] [ced] [ikl] [hny] [sw] [bgt] [ced] [il] [hny] [,.] [ced] [op] [mu] [] [
] [ ] [
] [ ] [] [a] [ced] [jmu] [ikl] [hny] [] [-sw] [op] [jmu] [ced] [bgt] [hny] [ikl] [hny] [bgt] [] [
] [ ] [
] [ ] [] 
```
The first word was probably website (look at the end - ".com"), so we were not interested in that. The remaining
two words were somewhat challenging to guess, but eventually we found them: `admin` and `something`. Concatenated
togather, they were the flag.

###PL version

Za????czony plik .wav by?? zbyt cichy, ??eby cokolwiek us??yszec, ale wzmacniaj??c go przy u??yciu Audacity, zauwa??yli??my, ??e
by??o to nagranie osoby pisz??cej na klawiaturze. S??owa by??y rozr????nialne - spacja by??a znacznie d??u??szym d??wi??kiem od
pozosta??ych klawiszy. Te niestety by??y dla ludzkiego ucha nierozr????nialne.

Sprawdzili??my jednak reprezentacj?? tych d??wi??k??w w Audacity i na??o??yli??my niekt??re z nich na siebie w GIMPie. Rezultat:
![](http://i.imgur.com/royrw1X.png)

Pierwszy obrazek, to dwa d??wi??ki "S" na??o??one na siebie - wygl??daj?? jak jedna fala. Drugi - to "O" i "I" - mia?? niewielkie,
pikselowe wr??cz r????nice. Ostatni za?? - "N" i "A" - ujawni?? znacz??ce r????nice w d??wi??kach. Najwyra??niej im dalej klawisze
si?? od siebie znajduj?? na klawiaturze, tym wi??ksza jest r????nica w ich d??wi??kach.

W tym momencie doskonale wiedzieli??my, o co chodzi w zadaniu - nale??y dopasowa?? nieznane d??wi??ki z pocz??tku do znanych
z ko??ca nagrania. ??atwo powiedzie??, trudniej zrobi??. Ostatecznie, zrobili??my to nast??puj??co:
- wczytalli??my surowe dane z pliku i je sparsowali??my
- znale??li??my g??rki odpowiadaj??ce uderzeniom klawisza
- wyci??li??my oko??o 0.05-sekundowe kawa??ki wok???? ka??dej g??rki
- naprawili??my podany tekst z bloga - niekt??re litery pojawi??y si?? w tek??cie, ale nie w d??wi??ku, co psu??o dopasowywanie
- dla ka??dego nieznanego d??wi??ku, znajdowali??my znany o najlepszym dopasowaniu

W praktyce jednak, musli??my poprzesta?? na kilku mo??liwo??ciach dla ka??dego uderzenia - niekt??re klawisze mia??y bowiem
identyczny d??wi??k, co inne, nie pozwalaj??c tym samym na jednoznaczny odczyt. Wynik dzia??ania programu:
```
[] [] [ced] [frv] [ced] [ikl] [hny] [sw] [bgt] [ced] [il] [hny] [,.] [ced] [op] [mu] [] [
] [ ] [
] [ ] [] [a] [ced] [jmu] [ikl] [hny] [] [-sw] [op] [jmu] [ced] [bgt] [hny] [ikl] [hny] [bgt] [] [
] [ ] [
] [ ] [] 
```
Pierwsze s??owo to prawdopodobnie nazwa strony internetowej (??wiadczy o tym ko??c??wka ".com"), wi??c nie jeste??my tym
fragmentem zainteresowani. Pozosta??e dwa s??owa to login i has??o - po d??u??szej chwili, zauwa??yli??my, ??e pasuj?? do
nich s??owa: `admin` i `something`. Po????czone razem, by??y one flag??.
