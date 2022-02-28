# lukas-skywalker-business (190pts, 32 solved) Forensics [Easy]

## First look
When we open the wav file, we can listen to some audio. I tried to find something in the spectogram, tried different tools etc.

## Solving
Eventually, I decided to try `LSB` and after trying a few different scripts, I found this one:
```python
import wave
song = wave.open("luke_skywalker_business.wav", mode='rb')
# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extract the LSB of each byte
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# Convert byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string.split("###")[0]

# Print the extracted text
print("Sucessfully decoded: "+decoded)
song.close()
```
Which gives us the following morse code:
```
.. -. ....... --- .-. -.. . .-. ....... - --- ....... .--. .-. --- - . -.-. - ....... .. - ....... ..-. .-. --- -- ....... - .... .. . ...- . ... ....... - .... .. ... ....... ... --- -. --. ....... .-- .- ... ....... .--. .-. --- - . -.-. - . -.. ....... .-- .. - .... ....... .- ....... ... . -.-. .-. . - ....... .--. .- ... ... .-- --- .-. -.. .-.-.- ....... - .... . ....... .--. .- ... ... .-- --- .-. -.. ....... .. ... ---... ....... -.-. - ..-. ..-. --... ----. ----. ..--- -.... -.-. ----- .---- -.. -.-. -.... -.. ..-. -.-. ..--- -.-. ...-- -... ..... -.... ..--- ----- --... ..--- -.-. ---.. -... ---.. -.... ...-- ..... ...-- . .---- . ..-. -.... -... ....- .---- ..-. ----. ..-. ...-- .---- ....- . .- ---.. ..--- -.... ...-- ----. ..-. -... ..... .- ----- ..... . -.... ..... ----.
```
Decoding this, gives:
```
IN ORDER TO PROTECT IT FROM THIEVES THIS SONG WAS PROTECTED WITH A SECRET PASSWORD. THE PASSWORD IS: CTFF79926C01DC6DFC2C3B562072C8B86353E1EF6B41F9F314EA82639FB5A05E659
```
Which has our flag: `CTF{F79926C01DC6DFC2C3B562072C8B86353E1EF6B41F9F314EA82639FB5A05E659}`