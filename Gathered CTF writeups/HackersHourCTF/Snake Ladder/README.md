# Hackers Hour CTF Snake&Ladder Writeup

Here is my writeup for the Snake & Ladder problem from Hackers Hour CTF, an Awesome CTF Event organized by The Hackers Meetup initiative by ComExpo Cyber Security Supported by Centre of Cyber and Information Security. This problem was the least solved challenge in the whole competition, with our team being the one and only solve.

## Problem Statement:
![](https://github.com/csn3rd/HackersHourCTFSnakeLadderWriteup/blob/master/Screen%20Shot%202020-09-29%20at%209.51.08%20AM.png)

## Snake&Ladder.txt
part-1 

11445 14555 45226 62343 62355 22151 22234 51633 32154 44651 34645 55234 32462

key-
2574423355631

## Solution
Since this challenge falls under the OSINT category, let's do some research on the problem title. According to Wikipedia,
```Snakes and Ladders, known originally as Moksha Patam, is an ancient Indian board game for two or more players regarded today as a worldwide classic. It is played on a game board with numbered, gridded squares. A number of "ladders" and "snakes" are pictured on the board, each connecting two specific board squares. The object of the game is to navigate one's game piece, according to die rolls, from the start (bottom square) to the finish (top square), helped by climbing ladders but hindered by falling down snakes.```

Let's keep this in our notes and go through the problem statement. An interesting piece of information in the problem statement which seems to be a hint is "ludo". If we look that up on Wikipedia, we find out that
```Ludo (from Latin ludo, meaning 'I play') is a strategy board game for two to four players, in which the players race their four tokens from start to finish according to the rolls of a single die. Like other cross and circle games, Ludo is derived from the Indian game Pachisi, but simpler. The game and its variations are popular in many countries and under various names.```

From these two descriptions, it seems like the challenge is making a reference towards two popular board games.

Next, we can download Snake&Ladder.txt and take a look at some code which we must decode and figure out. Just from inspection, the numbers in part 1 seem to be a polybius cipher of some sort. However, the numbers are in groups of 5 and the digits range from 1-6 rather than 1-5. Thinking back about the references to the board games, we can recognize that dice play an important role in both games as it is used to determine one's movement and placement in the games. We also know that dice have 6 sides and so these numbers may be referencing some set of dicerolls.

So, let's go on Google and search for "dice cryptography". A [wikipedia page](https://en.wikipedia.org/wiki/Diceware), titled Diceware, pops up.
```Diceware is a method for creating passphrases, passwords, and other cryptographic variables using ordinary dice as a hardware random number generator. For each word in the passphrase, five rolls of the dice are required. The numbers from 1 to 6 that come up in the rolls are assembled as a five-digit number, e.g. 43146. That number is then used to look up a word in a word list. In the English list 43146 corresponds to munch. By generating several words in sequence, a lengthy passphrase can be constructed.```

This looks like what we need for this challenge. The numbers in part 1 are in groups of 5 and all the digit fall between the range of 1-6. So, it seems we need to find a wordlist which contains corresponding values between numbers and words. Going deeper into the article, we learn that 
```The Electronic Frontier Foundation published three alternative English diceware word lists in 2016, further emphasizing ease-of-memorization with a bias against obscure, abstract or otherwise problematic words; one tradeoff is that typical EFF-style passphrases require typing a larger number of characters.```

Let's use the wordlist from the Electronic Frontier Foundation and see if this leads us anywhere. Here is the [wordlist](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt).

Let's match each number with its corresponding word:
```
11445 - alongside
14555 - cannot
45226 - pregnant
62343 - tingle
62355 - tinwork
22151 - danger
22234 - daydream
51633 - retake
32154 - geology
44651 - portfolio
34645 - jackal
55234 - snap
32462 - gossip
```

Now that we've matched each number in part 1 with its corresponding word, let's see if we can use the key to form a flag of some sort and test if we are using the correct wordlist. We realized that there are 13 words and the key is 13 characters long. Therefore, we can lineup each word along with a digit from the key.

```
alongside  - 2
cannot     - 5
pregnant   - 7
tingle     - 4
tinwork    - 4
danger     - 2
daydream   - 3
retake     - 3
geology    - 5
portfolio  - 5
jackal     - 6
snap       - 3
gossip     - 1
```

From here, we can try and take the designated character as defined by the key. So, for the first word, the corresponding digit is 2 so we take the second letter, which is 'l'. For the second word, the corresponding digit is 5 so we take the fifth letter which is 'o'. After doing this for the rest of the words,
```
alongside  - 2 - l
cannot     - 5 - o
pregnant   - 7 - n
tingle     - 4 - g
tinwork    - 4 - w
danger     - 2 - a
daydream   - 3 - y
retake     - 3 - t
geology    - 5 - o
portfolio  - 5 - f
jackal     - 6 - l
snap       - 3 - a
gossip     - 1 - g
```
we seemed to have formed a recognizable phrase, "long way to flag". We have decoded the numbers/codes in the file and reached the flag. From here, all we need to do is add underscores between words and wrap it in the flag format. 

## Flag

`THM{long_way_to_flag}`
