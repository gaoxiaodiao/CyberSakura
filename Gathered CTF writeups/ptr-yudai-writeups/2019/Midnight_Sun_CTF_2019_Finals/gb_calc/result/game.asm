; Disassembly of "gb-calc.gb"
; This file was created with mgbdis v1.3 - Game Boy ROM disassembler by Matt Currie.
; https://github.com/mattcurrie/mgbdis

ld_long: MACRO
    IF STRLWR("\1") == "a" 
        ; ld a, [$ff40]
        db $FA
        dw \2
    ELSE 
        IF STRLWR("\2") == "a" 
            ; ld [$ff40], a
            db $EA
            dw \1
        ENDC
    ENDC
ENDM

INCLUDE "hardware.inc"
INCLUDE "bank_000.asm"
INCLUDE "bank_001.asm"