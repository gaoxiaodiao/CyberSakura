# [pwn ???pts] tudutudututu2 - Byte Bandits CTF 2019
64bitです。
この問題名nullcon HackIMで見たぞ。
```
$ checksec -f pwnable
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	1		2	pwnable
```
tudutudututu同様にtopicを管理できるサービスです。

次のような構造体があります。
```c
typedef struct {
    char *topic;
    char *desc;
} st_topic;
```
createするときはdescに0が入れられます。
descriptionのサイズは自由に設定できますが、0xFFまでです。
deleteするときもちゃんとNULLかどうか調べてます。
```c
free(topic->topic);
if (topic->desc) {
    free(topic->desc);
}
free(topic);
```

writeupもないし方針が立たない......

# 感想
わかんなーい。