﻿## Reverse 200 (re, 200p)

### PL
[ENG](#eng-version)

Dostajemy [program](./r200) (elf konkretnie), który, podobnie jak poprzedni, wykonuje sprawdzenie hasła i odpowiada czy hasło jest poprawne czy nie.

Domyślamy się że poprawne hasło jest flagą.

Cały program to coś w rodzaju:

    int main() {
        printf("Enter the password: ");
        if (fgets(&password, 255, stdin)) {
            if (check_password(password)) {
              puts("Incorrect password!");
            } else {
              puts("Nice!");
            }
        }
    }

Patrzymy więc w funkcję check_password. W bardzo dużym uproszczeniu (tak naprawde nie było tu żadnych funkcji wywoływanych, wszystko inlinowane:

    bool check_password(char *password) {
        int buf[6];
        int reqired[6] = { 5, 2, 7, 2, 5, 6 };
        for (int i = 0; i <= 5; i++) {
            buf[i] = get_from_assoc(list, password[i]);
        }
        for (int i = 0; i <= 5; i++) {
            if (buf[i] != required[i]) {
                return true;
            }
        }
        return false;
    }

Gdzie list to globalna zmienna - lista asocjacyjna, wyglądająca mniej więcej tak (w nie-C składni):

    {
        'm': 0,
        'n': 1,
        'o': 2,
        'p': 3,
        'q': 4,
        'r': 5,
        's': 6,
        't': 7,
        'u': 8,
        'v': 9,
        'w': 10,
        'x': 11,
        'y': 12,
        'z': 13
    }

Z tego odczytaliśmy wymagane hasło - "rotors".

### ENG version

We get a [binary](./r200) (elf to be exact), which, as previously, performs a password check and returns if the password was correct or not,

We expect the password to be the flag.

The code is something like:

    int main() {
        printf("Enter the password: ");
        if (fgets(&password, 255, stdin)) {
            if (check_password(password)) {
              puts("Incorrect password!");
            } else {
              puts("Nice!");
            }
        }
    }

We look at the check_password function. Simplified version (there were no function calls, all inlined):

    bool check_password(char *password) {
        int buf[6];
        int reqired[6] = { 5, 2, 7, 2, 5, 6 };
        for (int i = 0; i <= 5; i++) {
            buf[i] = get_from_assoc(list, password[i]);
        }
        for (int i = 0; i <= 5; i++) {
            if (buf[i] != required[i]) {
                return true;
            }
        }
        return false;
    }

Where list is a global variable - associative container containing:

    {
        'm': 0,
        'n': 1,
        'o': 2,
        'p': 3,
        'q': 4,
        'r': 5,
        's': 6,
        't': 7,
        'u': 8,
        'v': 9,
        'w': 10,
        'x': 11,
        'y': 12,
        'z': 13
    }

We used it to read the password - "rotors".
