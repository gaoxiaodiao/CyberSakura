; Disassembly of "gb-calc.gb"
; This file was created with mgbdis v1.3 - Game Boy ROM disassembler by Matt Currie.
; https://github.com/mattcurrie/mgbdis

SECTION "ROM Bank $000", ROM0[$0]

RST_00::
    ret


    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

RST_08::
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

RST_10::
    add b
    ld b, b
    jr nz, jr_000_0024

    ld [$0204], sp
    db $01

RST_18::
    ld bc, $0402
    ld [$2010], sp
    ld b, b
    add b

RST_20::
    rst $38
    rst $38
    rst $38
    rst $38

jr_000_0024:
    rst $38
    rst $38
    rst $38
    rst $38

RST_28::
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

RST_30::
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

RST_38::
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

VBlankInterrupt::
    push hl
    ld hl, $c7b1
    jp Jump_000_0067


    rst $38

LCDCInterrupt::
    push hl
    ld hl, $c7c1
    jp Jump_000_0067


    rst $38

TimerOverflowInterrupt::
    push hl
    ld hl, $c7d1
    jp Jump_000_0067


    rst $38

SerialTransferCompleteInterrupt::
    push hl
    ld hl, $c7e1
    jp Jump_000_0067


    rst $38

JoypadTransitionInterrupt::
    push hl
    ld hl, $c7f1
    jp Jump_000_0067


Jump_000_0067:
    push af

    push bc
    push de

jr_000_006a:
    ld a, [hl+]
    or [hl]
    jr z, jr_000_0079

    push hl
    ld a, [hl-]
    ld l, [hl]
    ld h, a
    call Call_000_007e
    pop hl
    inc hl
    jr jr_000_006a

jr_000_0079:
    pop de
    pop bc
    pop af
    pop hl
    reti


Call_000_007e:
    jp hl


    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

Boot::
    nop
    jp Jump_000_0150


HeaderLogo::
    db $ce, $ed, $66, $66, $cc, $0d, $00, $0b, $03, $73, $00, $83, $00, $0c, $00, $0d
    db $00, $08, $11, $1f, $88, $89, $00, $0e, $dc, $cc, $6e, $e6, $dd, $dd, $d9, $99
    db $bb, $bb, $67, $63, $6e, $0e, $ec, $cc, $dd, $dc, $99, $9f, $bb, $b9, $33, $3e

HeaderTitle::
    db "CALC", $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00

HeaderNewLicenseeCode::
    db $00, $00

HeaderSGBFlag::
    db $00

HeaderCartridgeType::
    db $00

HeaderROMSize::
    db $00

HeaderRAMSize::
    db $00

HeaderDestinationCode::
    db $00

HeaderOldLicenseeCode::
    db $00

HeaderMaskROMVersion::
    db $01

HeaderComplementCheck::
    db $d3

HeaderGlobalChecksum::
    db $09, $6e

Jump_000_0150:
    di
    ld d, a
    xor a
    ld sp, $e000
    ld hl, $dfff
    ld c, $20
    ld b, $00

jr_000_015d:
    ld [hl-], a
    dec b
    jr nz, jr_000_015d

    dec c
    jr nz, jr_000_015d

    ld hl, $feff
    ld b, $00

jr_000_0169:
    ld [hl-], a
    dec b
    jr nz, jr_000_0169

    ld hl, $ffff
    ld b, $80

jr_000_0172:
    ld [hl-], a
    dec b
    jr nz, jr_000_0172

    ld a, d
    ld [$c7a8], a
    call $4853
    xor a
    ldh [rSCY], a
    ldh [rSCX], a
    ldh [rSTAT], a
    ldh [rWY], a
    ld a, $07
    ldh [rWX], a
    ld bc, $ff80
    ld hl, $486a
    ld b, $0a

jr_000_0192:
    ld a, [hl+]
    ld [c], a
    inc c
    dec b
    jr nz, jr_000_0192

    ld bc, $482b
    call $47e2
    ld bc, $4874
    call $47f4
    ld a, $e4
    ldh [rBGP], a
    ldh [rOBP0], a
    ld a, $1b
    ldh [rOBP1], a
    ld a, $c0
    ldh [rLCDC], a
    xor a
    ldh [rIF], a
    ld a, $09
    ldh [rIE], a
    xor a
    ldh [rNR52], a
    ldh [rSC], a
    ld a, $66
    ldh [rSB], a
    ld a, $80
    ldh [rSC], a
    xor a
    call $5e63
    ei
    call $493e
    daa
    ld [hl], $01
    nop

jr_000_01d2:
    db $76
    jr jr_000_01d2

    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ret


    rst $38
    rst $38
    rst $38
    jp $5bbe


    rst $38
    jp $527c


    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

Call_000_0200:
    add sp, -$06
    ld hl, sp+$08
    ld a, [hl]
    ld hl, sp+$04
    ld [hl+], a
    ld [hl], $00

Jump_000_020a:
    ld hl, sp+$09
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, sp+$05
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    ld e, a
    ld a, [de]
    ld c, a
    xor a
    or c
    jp z, Jump_000_0287

    ld a, c
    xor $80
    cp $b0
    jp nc, Jump_000_0233

    ld a, c
    xor $80
    cp $b9
    jp c, Jump_000_0281

Jump_000_0233:
    ld de, $c760
    ld hl, sp+$05
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    ld a, c
    add $d0
    ld c, a
    rla
    sbc a
    ld b, a
    sla c
    rl b
    ld hl, $001b
    add hl, bc
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl+]
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld [de], a
    inc hl
    inc hl
    ld a, [hl]
    dec hl
    add [hl]
    ld hl, sp+$00
    ld [hl], a
    ld de, $c760
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    ld a, c
    add $1c
    ld c, a
    ld a, b
    adc $00
    ld b, a
    ld a, c
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld [de], a

Jump_000_0281:
    ld hl, sp+$05
    inc [hl]
    jp Jump_000_020a


Jump_000_0287:
    add sp, $06
    ret


    ld l, b
    ld bc, $0014
    ld [de], a
    nop
    ld [hl], b
    ld a, [bc]
    and a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0302
    inc b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    dec b
    ld b, $07
    ld [$0908], sp
    ld a, [bc]
    dec bc
    inc c
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    dec c
    ld c, $08
    ld [$0808], sp
    ld [$0808], sp
    ld [$100f], sp
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld de, $1312
    inc d
    dec d
    ld d, $17
    jr jr_000_02f5

    ld a, [de]
    dec de
    inc e
    dec e
    ld e, $00
    nop
    nop
    nop
    nop
    rra
    jr nz, jr_000_030a

    ld [hl+], a
    inc hl
    inc h
    dec h
    ld h, $27
    jr z, jr_000_02f9

    ld [$0808], sp
    add hl, hl

jr_000_02f5:
    ld a, [hl+]
    nop
    nop
    nop

jr_000_02f9:
    nop
    dec hl
    inc l
    inc l
    inc l
    inc l
    dec l
    ld l, $2c
    inc l
    cpl
    jr nc, jr_000_0337

    ld [hl-], a
    ld [$3308], sp

jr_000_030a:
    nop
    nop
    nop
    nop
    inc [hl]
    inc l
    dec [hl]
    ld [hl], $2c
    scf
    jr c, jr_000_0342

    inc l
    inc l
    inc l
    add hl, sp
    ld a, [hl-]
    dec sp
    inc a
    dec a
    nop
    nop
    nop
    ld a, $3f
    ld b, b
    ld b, c
    ld b, d
    ld b, e
    ld b, h
    ld b, l
    ld b, [hl]
    ld b, a
    ld c, b
    ld c, c
    ld c, c
    ld c, d
    ld c, e
    ld c, h
    ld c, l
    ld c, [hl]
    nop
    nop
    ld c, a
    ld d, b

jr_000_0337:
    ld d, c
    ld d, d
    ld d, e
    ld d, h
    ld d, l
    ld d, [hl]
    ld d, a
    ld e, b
    ld e, c
    ld e, d
    ld e, e

jr_000_0342:
    ld e, h
    ld e, l
    ld e, [hl]
    ld e, a
    ld h, b
    nop
    nop
    ld h, c
    inc l
    ld h, d
    ld b, e
    ld b, e
    ld h, e
    ld h, h
    ld h, l
    ld h, [hl]
    ld h, a
    ld l, b
    ld l, c
    ld l, d
    ld b, e
    ld b, e
    ld l, e
    ld l, h
    ld l, l
    nop
    nop
    ld l, [hl]
    ld l, a
    ld [hl], b
    ld b, e
    ld b, e
    ld [hl], c
    ld [hl], d
    ld [hl], e
    ld [hl], h
    ld [hl], l
    db $76
    ld [hl], a
    ld a, b
    ld b, e
    ld b, e
    ld a, c
    ld a, d
    ld a, e
    nop
    nop
    nop
    ld a, h
    ld a, l
    ld a, [hl]
    ld a, [hl]
    ld a, [hl]
    ld a, [hl]
    ld a, [hl]
    ld a, a
    add b
    add c
    add d
    ld a, [hl]
    ld a, [hl]
    ld a, [hl]
    add e
    add h
    nop
    nop
    nop
    nop
    add l
    ld [$0808], sp
    ld [$0808], sp
    ld [$0808], sp
    ld [$0808], sp
    ld [$8608], sp
    nop
    nop
    nop
    nop
    add a
    adc b
    ld [$0808], sp
    adc c
    adc d
    adc e
    adc h
    adc l
    adc [hl]
    adc a
    ld [$9008], sp
    sub c
    nop
    nop
    nop
    nop
    nop
    sub d
    sub e
    ld [$9408], sp
    ld [$0808], sp
    ld [$0808], sp
    ld [$9695], sp
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sub a
    sbc b
    ld [$0808], sp
    ld [$0808], sp
    ld [$9908], sp
    sbc d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sbc e
    sbc h
    sbc l
    sbc [hl]
    ld [$9f08], sp
    and b
    and c
    and d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    and e
    and h
    and l
    and [hl]
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc bc
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sbc a
    ld a, a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld hl, sp-$01
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ret nz

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rlca
    inc bc
    rra
    rrca
    ld a, a
    ccf
    rst $38
    rst $38
    nop
    nop
    ld bc, $3f03
    rra
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld e, a
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld_long a, $fffc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    add b
    ret nz

    db $fc
    ld hl, sp-$01
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ldh [$c0], a
    ld hl, sp-$10
    cp $fc
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0701
    inc bc
    rrca
    rlca
    inc bc
    inc bc
    rlca
    rrca
    rra
    rra
    ld a, a
    ccf
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ret nz

    ret nz

    ldh [$f0], a
    ld hl, sp-$08
    db $fc
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    add b
    ldh [$c0], a
    ldh [$f0], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0300
    ld bc, $0303
    rlca
    rlca
    rra
    rrca
    ccf
    rra
    ld a, a
    ccf
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $fc
    rst $38
    ldh a, [rIE]
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld hl, sp-$01
    rrca
    rst $38
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld hl, $ffdf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $eb
    ldh a, [$fd]
    di
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $ed
    inc de
    ld sp, $fffe
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp b
    add $86
    ld a, c
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld h, b
    rra
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    jp nz, $e6ff

    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld [hl], a
    adc a
    ld h, c
    sbc [hl]
    cp $ff
    rst $38
    rst $38
    rst $00
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ldh a, [$f8]
    ld hl, sp-$04
    db $fc
    cp $fe
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    ret nz

    add b
    ret nz

    ret nz

    ldh [$e0], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0700
    rrca
    rra
    rrca
    ccf
    rra
    ccf
    ccf
    ccf
    ld a, a
    ld a, b
    ld a, a
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $fd
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld bc, $00ff
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, [$f8ff]
    rst $38
    ldh a, [rIE]
    ld hl, sp-$01
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rla
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc bc
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld c, a
    rst $38
    ldh a, [$f0]
    ldh a, [$f8]
    db $fc
    ld hl, sp-$04
    db $fc
    db $fc
    cp $ff
    cp $ff
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    ld bc, $0001
    inc bc
    ld [bc], a
    inc bc
    inc b
    inc bc
    nop
    rlca
    nop
    rrca
    nop
    rrca
    db $10
    rrca
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    inc bc
    rst $38
    rlca
    rst $38
    ld hl, sp-$01
    ld hl, sp-$01
    ld hl, sp-$01
    ld hl, sp-$01
    add sp, -$01
    xor b
    rst $38
    ld hl, sp-$01
    ld hl, sp-$01
    ld bc, $00ff
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rra
    rst $38
    inc bc
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rra
    rst $38
    rlca
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rlca
    rst $38
    inc bc
    rst $38
    add b
    add b
    add b
    ret nz

    ret nz

    ret nz

    ret nz

    ldh [$f0], a
    ldh [$e0], a
    ldh a, [$f0]
    ldh a, [$f0]
    ld hl, sp+$00
    rra
    nop
    rra
    nop
    ccf
    nop
    ccf
    nop
    ccf
    ld b, b
    ccf
    nop
    ld a, a
    nop
    ld a, a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ldh [rIE], a
    ld b, b
    rst $38
    inc c
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ret nz

    rst $38
    ret nz

    rst $38
    nop
    rst $38
    nop
    rst $38
    rlca
    rst $38
    rlca
    rst $38
    dec b
    rst $38
    dec b
    rst $38
    rlca
    rst $38
    rlca
    rst $38
    rrca
    rst $38
    rra
    rst $28
    ld hl, sp-$01
    ld hl, sp-$01
    jr z, @+$01

    xor b
    rst $38
    ld hl, sp-$01
    ld hl, sp-$01
    db $fc
    rst $38
    rst $38
    db $fc
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld bc, $00ff
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ret nz

    rst $38
    ld a, b
    rst $38
    ld e, $ff
    rlca
    rst $38
    ld a, a
    rst $38
    ccf
    rst $38
    rrca
    rst $38
    rlca
    rst $38
    rlca
    rst $38
    ld c, $ff
    inc e
    rst $38
    jr nc, @+$01

    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ccf
    rst $38
    rrca
    rst $38
    ld hl, sp-$08
    db $fc
    ld hl, sp-$04
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    cp $fe
    cp $fe
    cp $00
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0100
    nop
    nop
    nop
    nop
    ld a, a
    add b
    ld a, a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38

Jump_000_07f8:
    rst $38
    nop
    sbc a
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld bc, $03fe
    db $fc
    inc bc
    db $fc
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    rst $38
    inc de
    db $ec
    di
    inc c
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    dec bc
    db $f4
    ld a, a
    add b
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rrca
    rst $38
    rrca
    db $fd
    rrca
    ld sp, hl
    rrca
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    db $fc
    rst $38
    db $fc
    rst $38
    db $fc
    rst $20
    db $fc
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    db $fc
    inc bc
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    ret nz

    ccf
    db $fc
    inc bc
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ldh [$1f], a
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    inc bc
    rst $38
    ld bc, $01ff
    rst $38
    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    or b
    rst $38
    ldh [rIE], a
    ldh [rIE], a
    ret nz

    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    rst $38
    rra
    rst $38
    dec bc
    rst $38
    rrca
    rst $38
    rst $28
    rra
    rst $28
    rra
    rst $28
    rra
    rst $28
    rra
    rst $38
    cp $fe
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    nop
    add b
    nop
    nop
    add b
    add b
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0000
    ld bc, $0100
    nop
    ld bc, $0000
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    inc bc
    db $fc
    ld bc, $00fe
    rst $38
    inc bc
    nop
    inc bc
    nop
    ld [hl], e
    nop
    ccf
    nop
    ei
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld hl, sp+$00
    ld hl, sp+$00
    ld hl, sp+$00
    ld hl, sp+$00
    ld sp, hl
    nop
    ld sp, hl
    nop
    ld sp, hl
    nop
    ld sp, hl
    nop
    ld [c], a
    nop
    jp nz, $4200

    nop
    ld [bc], a
    nop
    ld [bc], a
    nop
    ld [hl+], a
    nop
    ld [c], a
    nop
    ld [c], a
    nop
    jr nz, jr_000_093e

jr_000_093e:
    ld h, $00
    daa
    nop
    daa
    nop
    daa
    nop
    daa
    nop
    ld h, $00
    jr nz, jr_000_094c

jr_000_094c:
    pop af
    nop
    ld sp, $3000
    nop
    stop
    ld [de], a
    nop
    ld [hl-], a
    nop
    inc sp
    nop
    di
    nop
    sbc c
    nop
    sbc c
    nop
    sbc c
    nop
    sbc c
    nop
    add hl, de
    nop
    add hl, de
    nop
    add hl, de
    nop
    add hl, de
    nop
    pop bc
    nop
    adc l
    nop
    rra
    nop
    stop
    stop
    inc e
    nop
    adc b
    nop
    pop bc
    nop
    adc h
    nop
    adc h
    nop
    adc h
    nop
    add b
    nop
    add b
    nop
    adc h
    nop
    adc h
    nop
    adc h
    nop
    add b
    nop
    di
    nop
    di
    nop
    di
    nop
    di
    nop
    di
    nop
    di
    nop
    di
    nop
    ld a, h
    nop
    ld sp, hl
    nop
    ld sp, hl
    nop
    ld hl, sp+$00
    db $fc
    nop
    rst $38
    nop
    ld sp, hl
    nop
    ld hl, sp+$00
    add hl, de
    nop
    sbc c
    nop
    ld sp, hl
    nop
    add hl, sp
    nop
    add hl, de
    nop
    sbc c
    nop
    jr jr_000_09ba

jr_000_09ba:
    inc a
    nop
    adc b
    nop
    adc b
    nop
    adc b
    nop
    adc b
    nop
    adc c
    nop
    adc c
    nop
    sbc c
    nop
    add hl, sp
    nop
    rst $08
    nop
    rst $08
    nop
    ld c, a
    nop
    ld c, a
    nop
    rrca
    nop
    rrca
    nop
    adc a
    nop
    rst $08
    nop
    rst $28
    rra
    rst $38
    rra
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    rst $38
    nop
    xor $01
    db $fc
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    rst $38
    rlca
    rst $38
    nop
    rst $38
    add b
    ld a, a
    nop
    rst $38
    rlca
    nop
    add b
    add b
    add b
    add b
    add b
    add b
    add b
    add b
    nop
    add b
    ld b, b
    add b
    ld b, b
    add b
    add b
    nop
    nop
    ld bc, $0102
    nop
    ld bc, $0100
    nop
    ld bc, $0100
    nop
    ld bc, $0100
    ld a, a
    add b
    ccf
    ret nz

    rrca
    ldh a, [rTAC]
    ld hl, sp+$03
    db $fc
    rrca
    db $fc
    inc bc
    db $fc
    inc bc
    db $fc
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    cp $00
    db $fc
    nop
    db $fc
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    ld a, a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld [$3900], sp
    nop
    add hl, sp
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rlca
    nop
    ld h, d
    nop
    ld a, [c]
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld b, $00
    ld h, a
    nop
    ld h, a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    inc e
    nop
    jr jr_000_0a9a

jr_000_0a9a:
    jr jr_000_0a9c

jr_000_0a9c:
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    nop
    sbc a
    nop
    adc a
    nop
    ldh [rP1], a
    and $18
    db $ed
    db $10
    rst $38
    rra
    rst $38
    rra
    rst $38
    rra
    rst $38
    rra
    rst $28
    db $10
    rlca
    nop
    rlca
    nop
    ld [hl], b
    nop
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    add b
    nop
    add b
    nop
    nop
    nop
    ld b, b
    add b
    add b
    add b
    add b
    add b
    add b
    add b
    add b
    nop
    nop
    ld bc, $0100
    ld bc, $0100
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ldh [rIE], a
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $08
    ccf
    sbc c
    and $ff
    rst $38
    rst $38
    ld a, a
    inc bc
    db $fc
    inc bc
    db $fc
    rst $20
    db $fc
    rst $38
    db $fc
    rst $38
    db $fc
    rst $08
    inc b
    rst $10
    ld hl, sp-$01
    db $fc
    db $fc
    nop
    db $fc
    nop
    db $fc
    nop
    cp $00
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld a, a
    nop
    rlca
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    jr c, jr_000_0b2e

jr_000_0b2e:
    add hl, sp
    nop
    add hl, sp
    nop
    add hl, sp
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    and $00
    adc $00
    sbc [hl]
    nop
    inc bc
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld h, a
    nop
    ld h, a
    nop
    ld h, a
    nop
    ld b, $00
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    inc e
    nop
    ld e, $00
    rra
    nop
    inc c
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rrca
    nop
    rra
    nop
    sbc a
    nop
    ccf
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $20
    rra
    rst $38
    rra
    rst $38
    rra
    rst $38
    rra
    rst $38
    rra
    rst $38
    rra
    ldh a, [rIF]
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $ff
    add b
    add b
    add b
    add b
    nop
    add b
    add b
    nop
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ccf
    ccf
    ccf
    ccf
    ccf
    ccf
    ccf
    rra
    rra
    rra
    rst $38
    db $fc
    rst $38
    db $fc
    rst $38
    db $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    call nz, $fffb
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rrca
    ldh a, [rIE]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld [c], a
    nop
    db $fc
    inc bc
    rst $38
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    adc [hl]
    nop
    sub $28
    cp $fe
    cp $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    ld hl, sp-$08
    ld hl, sp+$0f
    rra
    rrca
    rrca
    rrca
    rrca
    rrca
    rlca
    rlca
    rlca
    rlca
    inc bc
    inc bc
    inc bc
    ld bc, $f001
    ld hl, sp-$10
    ldh a, [$f0]
    ldh a, [$f0]
    ldh [$e0], a
    ldh [$e0], a
    ret nz

    ret nz

    ret nz

    add b
    add b
    nop
    ld bc, $0000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    ld a, a
    ld a, a
    ccf
    ccf
    ccf
    rra
    rrca
    rra
    rrca
    rrca
    rst $38
    rst $38
    rst $38
    rst $38
    xor [hl]
    add [hl]
    sbc [hl]
    or d
    cp [hl]
    cp d
    sbc [hl]
    or d
    xor [hl]
    add [hl]

jr_000_0c9a:
    cp a
    cp a
    rst $38
    rst $38
    rst $38
    rst $38
    and e
    ld sp, $ed6e
    pop bc
    ldh [$ef], a
    rst $28
    ldh [$f1], a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    add h
    adc [hl]
    ld a, l
    cp l
    ret c

    adc h
    db $ed
    push af
    inc b
    adc [hl]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld [hl], l
    jr nc, jr_000_0c9a

    or [hl]
    ld [hl], $17
    or $f7
    ld d, $37
    rst $38
    rst $38
    rst $18
    rst $18
    rst $18
    rst $18
    call z, $5b84
    db $dd
    ld e, [hl]
    call c, $df5f
    ld l, b
    call nz, $ffff
    rst $38
    rst $38
    rst $38
    rst $38
    ccf
    ld a, a
    rst $38
    rst $38
    rst $38
    ld a, a
    ld a, a
    cp a
    dec l
    ld l, l
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp a
    cp a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $ff
    cp $fe
    db $fc
    db $fc
    db $fc
    ld hl, sp-$08
    ld hl, sp-$10
    ldh a, [$80]
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rlca
    rlca
    inc bc
    inc bc
    ld bc, $0003
    ld bc, $0000
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    rst $38
    ccf
    ld a, a
    rra
    ccf
    rrca
    rra
    cp a
    cp a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fe
    db $fc
    db $fc
    ldh a, [$f8]
    ldh [$e0], a
    ldh [$c0], a
    add b
    ret nz

    nop
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rlca
    rrca
    rlca
    inc bc
    ld bc, $0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ccf
    ld a, a
    ccf
    rra
    rlca
    rrca
    inc bc
    inc bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    ld hl, sp-$08
    ldh a, [$f0]
    ret nz

    ret nz

    ldh [$f0], a
    ldh [$c0], a
    add b
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    ld a, a
    ccf
    rra
    rrca
    inc bc
    rlca
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ccf
    rra
    inc bc
    inc bc
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld e, a
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $ff
    ld hl, sp-$08
    ldh [$c0], a
    nop
    nop
    rst $38
    rst $38
    db $fc
    cp $f0
    ld hl, sp-$40
    ldh [rP1], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    nop

jr_000_0e1e:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc bc
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld a, a
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr nz, jr_000_0e1e

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld l, b
    ld bc, $0014
    ld [de], a
    nop
    ld [hl], b
    rlca
    ld [hl], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0302
    inc b
    dec b
    ld b, $07
    ld [$0000], sp
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add hl, bc
    ld a, [bc]
    dec bc
    inc c
    dec c
    ld c, $0f
    stop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld de, $1312
    inc d
    dec d
    ld d, $17
    jr jr_000_0ebe

jr_000_0ebe:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add hl, de
    ld a, [de]
    dec de
    nop
    inc e
    dec e
    ld e, $1f
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr nz, jr_000_0edf

jr_000_0edf:
    ld hl, $2322
    nop
    inc h
    dec h
    ld h, $00
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    daa
    jr z, @+$2b

    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    dec hl
    jr z, jr_000_0f28

    nop
    nop
    nop
    nop
    nop
    nop
    dec l
    ld l, $2f
    jr nc, @+$32

    jr nc, @+$32

    jr nc, jr_000_0f3b

    jr nc, jr_000_0f3d

    ld sp, $322e
    inc sp
    nop
    nop
    nop
    inc [hl]
    dec [hl]
    dec l
    ld l, $2f
    jr nc, jr_000_0f51

    scf
    jr c, jr_000_0f57

    ld a, [hl-]
    dec sp
    jr nc, jr_000_0f53

    ld l, $2e
    ld l, $3c
    dec a
    dec a

jr_000_0f28:
    ld a, $3f
    dec l
    ld l, $2f
    jr nc, jr_000_0f6f

    ld b, c
    ld b, d
    ld b, e
    ld b, h
    ld b, l
    jr nc, jr_000_0f67

    ld l, $2e
    ld l, $2e
    ld b, [hl]

jr_000_0f3b:
    ld b, [hl]
    ld b, a

jr_000_0f3d:
    ld c, b
    dec l
    ld l, $2f
    jr nc, jr_000_0f8c

    ld c, d
    ld c, e
    jr nc, jr_000_0f93

    jr nc, jr_000_0f79

    ld sp, $2e2e
    ld c, l
    ld c, [hl]
    ld c, a
    ld c, a
    ld d, b

jr_000_0f51:
    ld d, c
    ld d, d

jr_000_0f53:
    ld d, e
    ld d, h
    ld d, l
    ld d, l

jr_000_0f57:
    ld d, l
    ld d, l
    ld d, l
    ld d, l
    ld d, l
    ld d, l
    ld d, [hl]
    ld d, a
    ld e, b
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_0f67:
    nop
    ld e, c
    ld e, d
    ld e, e
    ld e, h
    ld e, l
    ld e, [hl]
    ld e, a

jr_000_0f6f:
    ld h, b
    ld h, c
    ld h, d
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_0f79:
    nop
    nop
    nop
    ld h, e
    ld h, h
    ld h, l
    ld h, [hl]
    ld h, a
    ld l, b
    ld l, c
    ld l, d
    ld l, e
    ld l, h
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_0f8c:
    nop
    nop
    nop
    nop
    ld l, l
    ld l, [hl]
    ld l, a

jr_000_0f93:
    ld [hl], b
    ld [hl], c
    ld [hl], d
    ld [hl], e
    ld [hl], h
    ld [hl], l
    halt
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_0fe2:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add d
    nop
    jp $c382


    add d
    jp $4382


    cp $bf
    jp nz, RST_00

    nop
    nop
    ld b, $00
    ld b, $06
    rlca
    ld c, $0f
    add hl, bc
    add hl, de
    add hl, bc
    add hl, bc
    rra
    nop
    nop
    nop
    nop
    inc bc
    nop
    ld [bc], a
    rlca
    inc b
    inc c
    inc c
    ld [$0888], sp
    ld [$0088], sp
    nop
    nop
    nop
    ld h, c
    add b
    inc sp
    pop hl
    ld [bc], a
    ld bc, $0102
    inc bc
    ld bc, $0103
    nop
    nop
    nop
    nop
    jr jr_000_1034

jr_000_1034:
    jr @+$32

    ld [hl], b
    jr nz, jr_000_1099

    ret nz

    add b
    ret nz

    jr nz, @-$3e

    nop
    nop
    nop
    nop
    call nz, $8600
    add $06
    rst $00
    rlca
    push bc
    inc b
    call nz, $c404
    nop
    nop
    nop
    nop
    ld [$1800], sp
    ld [$0818], sp
    jr jr_000_0fe2

    sbc b
    ret z

    ld hl, sp+$48
    nop
    nop
    nop
    nop
    ld [hl], $08
    ld hl, $e07e
    ld b, b
    add b
    ret nz

    add $80
    ret nz

    add a
    jp $c382


    add d
    ld b, c
    add d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rla
    jr jr_000_1081

jr_000_1081:
    jr nc, jr_000_1093

    jr nz, jr_000_1085

jr_000_1085:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    adc h
    dec b
    add $c4

jr_000_1093:
    ld b, e
    ld bc, $0000
    nop
    nop

jr_000_1099:
    nop
    nop
    nop
    nop
    nop
    ld [bc], a
    ld bc, $01f2
    ld [de], a
    pop hl
    ret nz

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld e, $00
    ld [hl], b
    jr nz, jr_000_10e9

    db $10
    inc d
    ld [$0000], sp
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc b
    call nz, $c404
    ld b, b
    add h
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld l, b
    jr c, jr_000_1109

    jr jr_000_10d3

jr_000_10d3:
    jr jr_000_10d5

jr_000_10d5:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld b, e
    pop bc
    ld d, l
    ld h, e
    ld bc, $0c3e
    nop
    nop
    nop
    nop

jr_000_10e9:
    nop
    nop
    nop
    nop
    nop
    ccf
    ld a, a
    cpl
    ld [hl], b
    jr nz, jr_000_1154

    jr nz, jr_000_1156

    jr nz, jr_000_1158

    jr nz, jr_000_115a

    jr nz, jr_000_115c

    jr nz, jr_000_115e

    ldh a, [$f0]
    ldh a, [rP1]
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1109:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0307
    rrca
    ld b, $0c
    inc c
    inc c
    jr jr_000_112b

    jr jr_000_1155

    db $10
    cp a
    ld a, a
    sbc $e1
    nop
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_112b:
    nop
    nop
    nop
    nop
    ret nz

    ldh a, [$e0]
    ld [hl], b
    jr c, @+$0a

    inc e
    inc b
    ld c, $03
    ld b, $06
    inc bc
    ld bc, $0003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    nop
    ld a, a
    rst $38
    ld e, [hl]
    pop hl
    ld b, b
    ret nz

jr_000_1154:
    ld b, b

jr_000_1155:
    ret nz

jr_000_1156:
    ld b, b
    ret nz

jr_000_1158:
    ld b, b
    ret nz

jr_000_115a:
    ld b, b
    ret nz

jr_000_115c:
    ld b, b
    ret nz

jr_000_115e:
    nop
    ret nz

    ldh a, [$e0]
    ld [hl], b
    jr nc, @+$32

    jr jr_000_117f

    jr jr_000_1171

    jr jr_000_1173

    jr jr_000_1185

    jr @+$22

    ld h, b
    cpl

jr_000_1171:
    ld [hl], b
    ccf

jr_000_1173:
    ld a, a
    jr nc, jr_000_11d6

    jr nz, jr_000_11d8

    jr nz, @+$62

    jr nz, @+$62

    jr nz, @+$62

    nop

jr_000_117f:
    nop
    ldh [rP1], a
    ldh a, [$e0]
    nop

jr_000_1185:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr nc, jr_000_11c0

    jr nc, jr_000_11c2

    jr nz, jr_000_11c4

    jr nz, jr_000_11c6

    jr nc, jr_000_11c8

    db $10
    jr nc, jr_000_11d3

    db $10
    jr jr_000_11b6

    inc bc
    ld bc, $0103
    inc bc
    ld bc, $0103
    inc bc
    ld bc, $0301
    ld bc, $0603
    inc bc
    add b
    nop
    add b
    nop
    add b
    nop
    add b
    nop

jr_000_11b6:
    add b
    nop
    add b
    nop
    nop
    nop
    nop
    nop
    ld b, b
    ret nz

jr_000_11c0:
    ld b, b
    ret nz

jr_000_11c2:
    ld a, a
    rst $38

jr_000_11c4:
    ld a, [hl]
    pop bc

jr_000_11c6:
    ld b, b
    ret nz

jr_000_11c8:
    ld b, b
    ret nz

    ld b, b
    ret nz

    ld b, b

jr_000_11cd:
    ret nz

    jr nc, jr_000_1200

    ld [hl], b
    ldh [$80], a

jr_000_11d3:
    ret nz

    add b
    ret nz

jr_000_11d6:
    ret nz

    ld h, b

jr_000_11d8:
    ld [hl], b
    jr nz, jr_000_11eb

    jr nc, @+$1a

    jr jr_000_11ff

    ld h, b
    jr nz, jr_000_1242

    jr nz, jr_000_1244

    jr nz, jr_000_1246

    jr nz, jr_000_1248

    ld b, b
    jr nz, jr_000_11eb

jr_000_11eb:
    nop
    nop
    nop
    jr jr_000_11fc

    inc b
    ld c, $02
    rlca
    ld bc, $0103
    nop
    nop
    nop
    nop
    nop

jr_000_11fc:
    nop
    nop
    nop

jr_000_11ff:
    nop

jr_000_1200:
    nop
    nop
    nop
    nop
    and b
    ret nz

    rst $38
    rst $38
    ld c, [hl]
    ccf
    nop
    nop
    nop
    nop
    ld c, $06
    ld c, $0c
    inc a
    jr jr_000_11cd

    ld [hl], b
    ret nz

    ldh [$80], a
    nop
    nop
    nop
    nop
    nop
    ld b, b
    ret nz

    ld b, b
    ret nz

    ld b, b
    ret nz

    ld b, b
    ret nz

    ld b, b
    ret nz

    add b
    ld b, b
    nop
    nop
    nop
    nop
    jr jr_000_123c

    inc c
    inc c
    ld b, $06
    rlca
    ld [bc], a
    inc bc
    inc bc
    nop
    ld bc, $0000

jr_000_123c:
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1242:
    nop
    nop

jr_000_1244:
    nop
    nop

jr_000_1246:
    nop
    nop

jr_000_1248:
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rlca
    nop
    rrca
    nop
    rra
    nop
    rra
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld hl, sp+$07
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rra
    ldh [rP1], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ret nz

    nop
    ldh a, [rP1]
    ld hl, sp+$00
    ccf
    nop
    ccf
    nop
    ccf
    nop
    ccf
    nop
    ccf
    nop
    ccf
    nop
    ccf
    nop
    ccf
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rra
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$fc], a
    nop
    cp $00
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add b
    nop
    ret nz

    nop
    ldh [rP1], a
    ld hl, sp+$00
    cp $00
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ccf
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ldh [rP1], a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld bc, $06fe
    ld hl, sp+$0f
    ldh a, [rSC]
    db $fd
    rlca
    ld hl, sp+$1a
    pop hl
    inc a
    jp Jump_000_07f8


    cp $01
    adc e
    ld [hl], b
    inc bc
    db $fc
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ret nz

    ccf
    ld bc, $02fe
    db $fc
    ld bc, $00fe
    rst $38
    nop
    rst $38
    ld bc, $0efe
    ldh a, [rNR34]
    pop hl
    rst $38
    nop
    rrca
    nop
    rst $28
    db $10
    rra
    ldh [$7f], a
    add b
    di
    inc c
    ret nz

    ccf
    nop
    rst $38
    ldh [$1f], a
    ret nc

    rrca
    ldh [$1f], a
    add b
    ld a, a
    ldh a, [rIF]
    cp $01
    dec e
    ldh [rP1], a
    rst $38
    ret nz

    nop
    cp $00
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld a, a
    nop
    rst $38
    nop
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ld hl, sp+$00
    ld hl, sp+$00
    inc a

jr_000_13d3:
    ret nz

    inc e
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [$3c], a
    jp $8778


    ldh [$1f], a
    ld b, b
    cp a
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld bc, $00fe
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld b, b
    sbc a
    ld [hl], b
    adc a
    ld [hl], b
    adc a
    ld [hl], b
    adc a
    ldh [$1f], a
    ld d, b
    adc a
    jr nc, jr_000_13d3

    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    inc c
    di
    rrca
    ldh a, [rIF]
    ldh a, [rP1]
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    ld c, $f1
    ld c, $f1
    ld c, $f1
    ld c, $f1
    ld c, $f1
    nop
    rst $38
    rst $38
    nop
    cp $01
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    ldh [$1f], a
    inc e
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [rNR32], a
    ldh [$3c], a
    ret nz

    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld [hl], b
    adc a
    rst $38
    nop
    rst $38
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ldh a, [rIF]
    ldh a, [rIF]
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    ld c, $f1
    ld c, $f1
    ld c, $f1
    ld b, $f9
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    db $fc
    nop
    ldh a, [rP1]
    ret nz

    nop
    add b
    nop
    nop
    nop
    rst $38
    nop
    ldh [rP1], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    ld h, b
    nop
    rra
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld hl, sp+$00
    jr c, jr_000_14f2

jr_000_14f2:
    ldh [rP1], a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ccf
    nop
    ccf
    nop
    rra
    nop
    rra
    nop
    rrca
    nop
    rlca
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    ld hl, sp+$07
    ld hl, sp+$07
    ld hl, sp+$07
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    rra
    ldh [$1f], a
    ldh [$1f], a
    ldh [rIE], a
    nop
    rst $38
    nop
    rst $38
    nop
    nop
    nop
    nop
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    rst $38
    nop
    cp $00
    nop
    nop
    nop
    nop
    cp $00
    db $fc
    nop
    ld hl, sp+$00
    ldh a, [rP1]
    ret nz

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0100
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $1600
    nop
    db $10
    inc b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld [de], a
    add b
    db $10
    ld b, d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr jr_000_15aa

jr_000_15aa:
    ld b, $90
    db $10
    add d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc c
    nop
    ld [$301e], sp
    stop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr nz, jr_000_15ca

jr_000_15ca:
    ld sp, hl
    ld [hl], d
    ret nz

    sbc e
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld b, $00
    inc b
    ld l, a
    dec b
    ld l, a
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr jr_000_1604

    dec l
    jr jr_000_15ef

jr_000_15ef:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld h, e
    nop
    jp nc, $86e3

    add e
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1604:
    nop
    nop
    nop
    nop
    add b
    nop
    add b
    nop
    add b
    nop
    ld bc, $0000
    ld bc, $0000
    nop
    nop
    nop
    nop
    ld [bc], a
    ld bc, $0300
    inc bc
    ld bc, $0410
    ld d, h
    add e
    ld bc, $0000
    nop
    nop
    nop
    ld b, b
    adc c
    ld c, c
    ret


    adc c
    ret


    db $10
    ld b, d
    ld [de], a
    adc h
    nop
    add b
    nop
    nop
    nop
    nop
    or b
    ld bc, $b381
    ld [c], a
    di
    db $10
    add d
    ld [de], a
    sbc h
    nop
    nop
    nop
    nop
    nop
    nop
    ld [de], a
    inc c
    ld c, $9a
    sbc d
    adc [hl]
    add hl, sp
    db $10
    inc c
    ld e, $00
    nop
    nop
    nop
    nop
    nop
    sbc b
    ld b, b
    ld h, b
    ld [hl], b
    ld [hl], b
    jr nz, @-$3e

    sbc e
    db $e3
    ld [hl], c
    nop
    nop
    nop
    nop
    nop
    nop
    ld d, c
    jr nz, @-$7e

    ld b, c
    jp nz, $4601

    ld l, a
    db $e3
    call RST_00
    nop
    nop
    nop
    nop
    ld bc, $9118
    ld [$1889], sp
    dec l
    inc a
    ld a, [hl]
    inc h
    nop
    nop
    nop
    nop
    nop
    nop
    ld [bc], a
    nop
    inc de
    add d
    or a
    ld b, b
    sub [hl]
    or e
    ld h, a
    di
    nop
    nop
    nop
    nop
    nop
    nop
    dec b
    jr @+$03

    jr nz, jr_000_169d

jr_000_169d:
    ld hl, $0080
    nop
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    ld b, b
    add b
    nop
    nop
    ld b, b
    add b
    ld [bc], a
    ld bc, $0102
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld l, c
    ret


    nop
    ret


    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    and d
    ld [hl], a
    ld [de], a
    inc h
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sbc [hl]
    jp z, $4299

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jr nc, jr_000_1710

    db $10
    jr nz, jr_000_16f3

jr_000_16f3:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ret nz

    inc bc
    ld [hl], h
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    dec d
    adc b

jr_000_1710:
    inc b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld d, d
    dec h
    inc h
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    dec c
    inc h
    cp l
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ret nz

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld l, b
    ld bc, $0014
    ld [de], a
    nop
    db $10
    ld [bc], a
    ld hl, $0000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0302
    inc b
    dec b
    ld b, $07
    ld [$0a09], sp
    dec bc
    inc c
    dec c
    ld c, $0f
    stop
    nop
    nop
    nop
    ld de, $1312
    inc d
    dec d
    ld d, $17
    jr jr_000_1830

    ld a, [de]
    dec de
    inc e
    dec e
    ld e, $1f
    jr nz, jr_000_181f

jr_000_181f:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1830:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    db $fc
    ld hl, sp-$04
    ld hl, sp-$08
    ld hl, sp-$08
    ld hl, sp-$08
    ld hl, sp-$08
    ld b, c
    add b
    nop
    nop
    ld e, $3f
    ccf
    ld a, a
    rst $38
    ld a, a
    ld a, a
    rst $38
    ld [hl], b
    ldh a, [rSVBK]
    ldh a, [$7f]
    rst $38
    ld a, a
    ld a, [hl]
    ld a, [hl]
    ld a, [hl]
    db $fc
    cp $fe
    db $fc
    db $fc
    db $fc
    jr c, jr_000_197a

    jr c, @+$7a

    rrca
    rrca
    rrca
    rlca
    rlca
    rlca
    inc bc
    rlca
    rlca
    ld h, e
    ld h, e
    ld h, e
    pop hl
    ld h, e
    ld h, c
    pop af
    pop bc
    pop hl
    pop bc
    ldh [$c0], a
    ldh [$c0], a
    ldh [$c2], a
    ldh [$c2], a
    ld [c], a
    jp $c3e2


    db $e3
    ldh a, [$f8]
    ld hl, sp-$10
    ldh a, [$f0]
    ldh a, [$60]
    ld h, h
    ld h, b
    inc h
    ld b, h
    inc c
    inc b
    inc c
    inc c
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    inc bc
    inc bc
    inc bc
    inc bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc bc
    rlca
    inc bc
    rlca
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fe
    cp $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    and c
    ret nz

    nop
    nop
    ld e, $1c
    ld a, $3e
    ld a, [hl]
    ccf
    ccf
    ld a, a
    ccf
    ld a, a
    ccf
    ld a, a
    ld sp, hl
    ldh a, [$30]
    ld a, b
    jr c, jr_000_19ae

    inc e
    jr jr_000_1995

    inc e

jr_000_197a:
    inc c
    inc e
    inc c
    ld e, $0e
    ld e, $fe
    db $fc
    db $fc
    db $fc
    ld a, b
    db $fc
    ld hl, sp+$78
    ld a, b
    ld a, b
    jr c, jr_000_19fc

    jr nc, jr_000_19bf

    ld hl, $6031
    jr nc, jr_000_19b3

    ld [hl], b
    ld h, c

jr_000_1995:
    ld [hl], c
    pop hl
    ld [hl], c
    pop hl
    pop af
    ldh [$f0], a
    ldh [$f0], a
    pop hl
    pop af
    ld b, $07
    ld b, $07
    cp $ff
    cp $ff
    cp $ff
    ld b, $0f
    ld b, $0f

jr_000_19ae:
    cp $ff
    ld bc, $0000

jr_000_19b3:
    nop
    inc e
    inc e
    ld e, $1c
    ld e, $1c
    inc e
    inc e
    nop
    nop
    nop

jr_000_19bf:
    nop
    rst $38
    rst $38
    ld a, a
    ld a, a
    ld a, a
    ccf
    ccf
    ccf
    ld a, a
    ccf
    ccf
    ld a, a
    ld a, a
    rst $38
    ld a, a
    rst $38
    ld hl, sp-$08
    ld hl, sp-$04
    db $fc
    db $fc
    rst $38
    cp $ff
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $fc
    ld a, h
    ld a, h
    ld a, h
    inc e
    inc a
    nop
    nop
    ld b, c
    add b
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    jr c, jr_000_1a6a

    jr c, jr_000_1a64

    ld sp, $2171
    ld [hl], c
    ld [hl], e
    pop hl
    rst $38
    rst $38

jr_000_19fc:
    rst $38
    rst $38
    rst $38
    rst $38
    ld bc, $0101
    nop
    ld hl, sp-$08
    ld hl, sp-$08
    db $fc
    ld hl, sp-$01
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    jp $c3e3


    db $e3
    jp $43e3


    db $e3
    jp $ff63


    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc e
    inc c
    inc e
    sbc h
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    db $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    ld [hl], b
    ld a, b
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc bc
    inc bc
    inc bc
    inc bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $fc
    db $fc
    cp $fc
    cp $fe
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, [hl]
    ccf
    ld a, $3e

jr_000_1a64:
    ld e, $1c
    nop
    nop
    and c
    ret nz

jr_000_1a6a:
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rra
    ld e, $1e
    rra
    ccf
    ccf
    ccf
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc sp
    ld bc, $0301
    inc bc
    inc bc
    add a
    inc bc
    add a
    add a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    pop hl
    pop af
    pop hl
    pop af
    pop hl
    pop af
    ldh [$f0], a
    ldh [$f0], a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $ff
    cp $ff
    cp $ff
    ld b, $07
    ld b, $07
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    inc e
    jr jr_000_1acf

    inc e
    inc e
    ld e, $1e
    ld e, $1e
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    ld a, a
    ccf
    ccf
    rra
    ccf
    ccf
    rra
    rra
    rra
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

jr_000_1acf:
    rst $38
    nop
    inc b
    jr nz, jr_000_1ad4

jr_000_1ad4:
    jr nz, jr_000_1ad6

jr_000_1ad6:
    or b
    inc b
    ld c, e
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0002
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc bc
    inc b
    dec b
    ld b, $00
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rlca
    ld [$0a09], sp
    dec bc
    inc c
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    dec c
    ld c, $0f
    db $10
    ld de, $0012
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc de
    inc d
    dec d
    ld d, $17
    jr jr_000_1c17

jr_000_1c17:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add hl, de
    ld a, [de]
    dec de
    ld d, $1c
    dec e
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld e, $1f
    jr nz, jr_000_1c77

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld [hl+], a
    inc hl
    nop
    nop
    nop

jr_000_1c77:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc h
    dec h
    nop
    nop
    nop
    nop
    nop
    ld h, $27
    jr z, jr_000_1cfb

jr_000_1cfb:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add hl, hl
    ld a, [hl+]
    dec hl
    inc l
    dec l
    ld l, $2f
    jr nc, jr_000_1d45

    ld [hl-], a
    inc sp
    inc [hl]
    dec [hl]
    ld [hl], $37
    inc [hl]
    jr c, jr_000_1d56

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld a, [hl-]
    dec sp
    inc a
    dec a
    ld a, $3f
    ld b, b
    ld b, c
    ld b, d
    ld b, e
    ld b, h
    ld b, l
    ld b, [hl]
    ld b, a
    ld c, b
    ld b, l
    ld c, c
    ld c, d
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1d45:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_1d56:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $ff
    cp $fc
    ld hl, sp-$08
    ldh a, [$f0]
    add $ee
    rst $30
    ei
    jp $c3e3


    add a
    rlca
    rlca
    rlca
    rrca
    rra
    rrca
    rra
    rra
    rra
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fe
    db $fc
    ld hl, sp-$08
    ldh a, [$f0]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $00
    cp $06
    adc h
    inc e
    jr jr_000_1fad

    jr nc, jr_000_1fe7

    ld h, b
    ldh [$c0], a
    rst $08
    sbc [hl]
    sbc a
    ld a, $7c
    ld a, [hl]
    ld sp, hl
    ld a, l
    ld [hl], e
    ld a, e
    ld d, e
    daa
    rlca
    rrca
    rrca
    rra
    ccf
    ld a, a
    rst $38
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ret nz

    ret nz

    add b
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld a, a
    nop

jr_000_1fac:
    nop

jr_000_1fad:
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add a
    ld a, a
    ld bc, $0300
    ld bc, $0307
    ld c, $06
    inc e
    inc c
    jr c, jr_000_1fe0

    ld [hl], b
    jr nc, jr_000_1fac

    pop hl
    jp $87c3


    add [hl]
    ld c, $0c
    inc e
    jr @+$3a

    jr nc, jr_000_2047

    jr nz, jr_000_1fd9

jr_000_1fd9:
    nop
    ret nz

    add b
    add b
    nop
    nop
    nop

jr_000_1fe0:
    nop
    ld bc, $0103
    ld [bc], a
    rlca
    inc c

jr_000_1fe7:
    ld b, $18
    inc c
    ccf
    rra
    ld a, a
    ccf
    rst $08
    ld l, a
    sbc a
    rst $08
    rrca
    sbc a
    rra
    rra
    rra
    ccf
    ccf
    ld a, a
    nop
    add b
    ret nz

    add b
    add b
    ret nz

jr_000_2000:
    ldh [$c0], a
    ldh [$e0], a
    ldh a, [$e0]
    ldh a, [$f0]
    ld hl, sp-$10
    nop
    nop
    ld bc, $0300
    ld bc, $0307
    ld c, $06
    inc b
    inc c
    nop
    nop
    nop
    nop
    ldh [$60], a
    ret nz

    ret nz

    add b
    add b
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld bc, $0100
    nop
    nop
    nop
    nop
    nop
    nop
    db $10
    jr c, jr_000_209e

    jr nc, jr_000_2000

    ld h, c
    add e
    jp $8707


    rrca
    rrca
    dec de

jr_000_2047:
    rra
    scf
    inc sp
    rst $38
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    pop af
    ld hl, sp-$20
    ldh a, [$c0]
    ldh [$c0], a
    ret nz

    ldh [$c0], a
    ret nz

    ldh [$f8], a
    ld hl, sp-$08
    ld hl, sp-$08
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    ld [$0010], sp
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

jr_000_209e:
    ld bc, $0301
    inc bc
    rlca
    ld b, $0e
    inc c
    inc e
    jr @+$3a

    jr nc, jr_000_2122

    ld h, e
    rst $20
    jp $83c7


    add a
    inc bc
    rlca
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    ldh [$e0], a
    ldh [$f0], a
    rst $38
    ldh a, [rIE]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    nop
    nop
    nop
    nop
    nop
    db $fd
    rst $38
    rst $38
    rst $38
    cp $ff
    cp $fe
    cp $fc
    jr c, @+$32

    jr nc, jr_000_213e

    and $c6
    add $8c
    inc c
    sbc b
    jr @+$32

    ld [hl], b
    ld h, b
    ldh [$e0], a
    ld [hl], b
    ld h, b
    ld h, b
    ret nz

    ret nz

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    ld bc, $0103
    inc bc
    ld bc, $e003
    ldh [$f0], a
    ldh [$f0], a
    ldh [$f0], a
    ldh [$f0], a
    ldh [$e0], a
    ldh a, [$e0]
    ldh a, [$e0]
    ldh a, [rP1]
    nop
    ld [bc], a
    inc c
    rrca
    rrca
    rrca
    rrca

jr_000_2122:
    rrca
    rrca
    rrca
    rrca
    rrca
    rrca
    rlca
    rrca
    nop
    nop
    nop
    nop
    add b
    nop
    add b
    ret nz

    ldh [$f0], a
    ld hl, sp-$04
    cp $ff
    rst $38
    rst $38
    ld bc, $0103
    inc bc

jr_000_213e:
    inc bc
    ld bc, $0301
    rlca
    inc bc
    rrca
    rlca
    ld a, a
    adc a
    rst $38
    rst $38
    ldh [$f0], a
    ldh a, [$f0]
    ld hl, sp-$10
    cp $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rlca
    rrca
    rrca
    rrca
    rra
    rra
    ccf
    ccf
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    cp $fc
    cp $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    rst $38
    ld a, a
    rst $38
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld hl, sp-$10
    ldh [$e0], a
    jp $ffe7


    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    adc a
    rst $08
    adc a
    rst $08
    adc a
    rst $08
    rst $38
    rst $38
    rst $38
    rst $38
    ld hl, sp-$10
    ld hl, sp-$10
    ei
    pop af
    ei
    pop af
    ei
    pop af
    ei
    pop af
    rst $38
    rst $38
    rst $38
    rst $38
    ccf
    rra
    rra
    rrca
    rst $08
    adc [hl]
    adc $ce
    adc $ce
    adc $ce
    rst $38
    rst $38
    rst $38
    rst $38
    rst $00
    add e
    ld bc, $3001
    add hl, sp
    inc a

Jump_000_21e5:
    ld a, b
    ld a, b
    ld a, h
    inc a
    ld a, b
    rst $20
    rst $08
    rst $20
    rst $08
    ldh [$c0], a
    ldh [$c0], a
    rst $20
    rst $08
    rst $20
    rst $08
    rst $20
    rst $08
    rst $20
    rst $08
    cp $fc
    cp $fc
    cp $fc
    cp $fc
    cp $fc
    cp $fc
    cp $fc
    cp $fc
    ld a, [hl]
    db $fc
    ld a, [hl]
    db $fc
    ld c, $0c
    ld c, $0c
    ld a, [hl]
    db $fc
    ld a, [hl]
    db $fc
    ld a, [hl]
    db $fc
    ld a, [hl]
    db $fc
    rst $38
    ld a, a
    rst $38
    ld a, a
    rrca
    rlca
    rlca
    inc bc
    di
    ld h, e
    di
    ld [hl], e
    di
    ld [hl], e
    di
    ld [hl], e
    rst $38
    rst $38
    rst $38
    rst $38
    pop hl
    jp $8081


    cp h
    inc e
    nop
    nop
    nop
    nop
    rra
    ccf
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    cp $fc
    cp $fc
    ld a, [hl]
    db $fc
    ld a, [hl]
    db $fc
    cp $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rrca
    ld c, $0c
    inc c
    db $fd
    ld a, b
    ld hl, sp+$78
    ld hl, sp+$78
    ld hl, sp+$79
    rst $38
    rst $38
    rst $38
    rst $38
    ld c, $1f
    rrca
    rlca
    rst $20
    rst $20
    inc bc
    rlca
    ld [bc], a
    ld b, $fe
    cp $ff
    rst $38
    rst $38
    rst $38
    rrca
    rlca
    inc bc
    inc bc
    di
    di
    add c
    inc bc
    ld bc, $3103
    ld [hl], e
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $18
    adc a
    rst $28
    rst $00
    rst $28
    rst $00
    ldh [$c0], a
    ldh [$c0], a
    rst $28
    rst $00
    rst $28
    rst $00
    rst $28
    rst $00
    rst $28
    rst $00
    adc a
    rst $08
    adc a
    rst $08
    adc [hl]
    rst $08
    adc a
    rst $08
    adc a
    rst $08
    adc a
    rst $08
    adc [hl]
    adc $8e
    adc $ff
    rst $38
    rst $38
    rst $38
    ldh a, [$e0]
    ret nz

    ret nz

    adc $8e
    adc [hl]
    sbc [hl]
    sbc [hl]
    sbc [hl]
    sbc [hl]
    sbc [hl]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ei
    pop af
    ei
    pop af
    ei
    pop af
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $08
    adc $cf
    rst $08
    rst $08
    rst $08
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    jr nc, jr_000_2325

    ld bc, $c301
    add a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $20
    rst $00
    ret nz

    ldh [$e1], a
    ldh a, [rIE]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    db $fc
    cp $fe
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, [hl]
    ld a, h
    ld c, $0c
    ld e, $0c
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38

jr_000_2325:
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    di
    ld [hl], e
    di
    ld [hl], e
    di
    ld [hl], e
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    adc h
    rra
    add c
    add b
    db $e3
    pop bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    cp $fc
    cp $fc
    cp $fc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    db $fc
    ld a, b
    db $fc
    ld a, h
    rst $38
    ld a, [hl]
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld h, [hl]
    cp $0e
    ld b, $1f
    rrca
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    ld [hl], c
    ld [hl], e
    ld bc, $8103
    inc bc
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $08
    adc a
    add a
    rst $00
    rst $28
    rst $00
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $28
    rst $00
    rst $28
    rst $00
    rst $28
    rst $00
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    adc [hl]
    adc $c6
    add $c7
    rst $20
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    adc [hl]
    adc [hl]
    ret nz

    ret nz

    ret nz

    ldh [$bc], a
    sbc $c0
    add b
    ld [c], a
    pop bc
    rst $38
    rst $38
    rst $38
    rst $38
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    ld a, a
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    rst $38
    nop
    ld bc, $0101
    ld bc, $0101
    ld bc, $0101
    ld bc, $0101
    ld bc, $0101
    ld bc, $0101
    ld [bc], a
    inc bc
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    dec b
    inc bc
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    dec b
    ld b, $07
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    rlca
    ld [$0404], sp
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    inc b
    add hl, bc
    ld a, [bc]
    ld a, [bc]
    ld a, [bc]
    dec bc
    inc b
    inc b
    inc c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $04
    inc c
    dec c
    dec c
    dec c
    ld c, $04
    inc b
    rrca
    db $10
    ld de, $100f
    ld de, $100f
    ld de, $100f
    ld de, $0f04
    db $10
    db $10
    db $10
    ld de, $0404
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    inc b
    add hl, bc
    ld a, [bc]
    ld a, [bc]
    ld a, [bc]
    dec bc
    inc b
    inc b
    inc c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $04
    inc c
    dec c
    dec c
    dec c
    ld c, $04
    inc b
    rrca
    db $10
    ld de, $100f
    ld de, $100f
    ld de, $100f
    ld de, $0f04
    db $10
    db $10
    db $10
    ld de, $0404
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    add hl, bc
    ld a, [bc]
    dec bc
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $0c
    dec c
    ld c, $04
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    rrca
    db $10
    ld de, $100f
    ld de, $100f
    ld de, $100f
    ld de, $0404
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    add hl, bc
    ld a, [bc]
    dec bc
    inc b
    inc b
    inc b
    add hl, bc
    ld a, [bc]
    dec bc
    inc b
    add hl, bc
    ld a, [bc]
    ld a, [bc]
    ld a, [bc]
    dec bc
    inc b
    inc b
    inc b
    inc b
    inc b
    inc c
    dec c
    ld c, $04
    inc b
    inc b
    inc c
    dec c
    ld c, $04
    inc c
    dec c
    dec c
    dec c
    ld c, $04
    inc b
    inc b
    inc b
    inc b
    rrca
    db $10
    ld de, $0404
    inc b
    rrca
    db $10
    ld de, $0f04
    db $10
    db $10
    db $10
    ld de, $0404
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    inc b
    add hl, bc
    ld a, [bc]
    dec bc
    inc c
    dec c
    ld c, $0f
    db $10
    ld de, $0a09
    ld a, [bc]
    ld a, [bc]
    dec bc
    inc b
    inc c
    dec c
    dec c
    dec c
    ld c, $04
    rrca
    db $10
    db $10
    db $10
    ld de, $1204
    inc de
    inc d
    dec d
    ld d, $17
    jr jr_000_257e

    ld a, [de]
    ld [de], a
    inc de
    inc de
    inc de
    inc d
    inc b
    dec d
    ld d, $16
    ld d, $17
    inc b
    jr jr_000_258d

    add hl, de
    add hl, de
    ld a, [de]
    inc b
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp

jr_000_257e:
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    dec sp
    inc a
    inc a
    inc a

jr_000_258d:
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    inc a
    ld sp, $3332
    inc [hl]
    dec [hl]
    ld [hl], $37
    jr c, jr_000_25de

    jr nz, jr_000_25d7

    jr nz, @+$23

    ld d, b
    jp nz, Jump_000_21e5

    dec de
    ld [hl-], a
    push hl
    call $4eea
    add sp, $04
    ld hl, $2578
    push hl
    ld hl, $0212
    push hl
    ld hl, $0101
    push hl
    call $4fe3
    add sp, $06
    ret


Call_000_25c7:
    add sp, -$1f
    call $25a8
    ld c, $00

Jump_000_25ce:
    ld hl, sp+$21
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld l, c
    ld h, $00
    add hl, de

jr_000_25d7:
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    ld e, a

jr_000_25de:
    ld a, [de]
    or a
    jp z, Jump_000_25e7

    inc c
    jp Jump_000_25ce


Jump_000_25e7:
    ld a, c
    cp $12
    jp c, Jump_000_25f8

    ld a, c
    add $ee
    ld hl, sp+$1d
    ld [hl-], a
    ld [hl], $12
    jp Jump_000_25fe


Jump_000_25f8:
    ld hl, sp+$1d
    ld [hl], $00
    dec hl
    ld [hl], c

Jump_000_25fe:
    ld hl, sp+$1e
    ld [hl], $00

Jump_000_2602:
    ld hl, sp+$1e
    ld a, [hl]
    dec hl
    dec hl
    sub [hl]
    jp nc, Jump_000_263d

    ld hl, sp+$04
    ld b, l
    ld c, h
    ld e, b
    ld d, c
    ld hl, sp+$1e
    ld l, [hl]
    ld h, $00
    add hl, de
    ld b, l
    ld c, h
    ld hl, sp+$1e
    ld a, [hl]
    dec hl
    add [hl]
    ld hl, sp+$02
    ld [hl], a
    ld hl, sp+$21
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, sp+$02
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    ld e, a
    ld a, [de]
    ld e, b
    ld d, c
    ld [de], a
    ld hl, sp+$1e
    inc [hl]
    jp Jump_000_2602


Jump_000_263d:
    ld hl, sp+$04
    ld c, l
    ld b, h
    ld hl, sp+$1c
    ld l, [hl]
    ld h, $00
    add hl, bc
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $00
    ld [de], a
    push bc
    ld hl, sp+$1e
    ld a, [hl]
    push af
    inc sp
    call Call_000_0200
    add sp, $03
    ld a, $13
    ld hl, sp+$1c
    sub [hl]
    ld c, a
    ld hl, $c760
    push hl
    ld a, $02
    push af
    inc sp
    ld hl, sp+$1f
    ld a, [hl]
    push af
    inc sp
    ld a, $01
    push af
    inc sp
    ld a, c
    push af
    inc sp
    call $4fe3
    add sp, $06
    add sp, $1f
    ret


Call_000_2681:
    add sp, -$04
    ld a, $03
    ld hl, sp+$06
    sub [hl]
    jp c, Jump_000_26d2

    ld a, $03
    inc hl
    sub [hl]
    jp c, Jump_000_26d2

    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    ld c, l
    ld b, h
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    ld hl, sp+$06
    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0001
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld b, [hl]
    ld hl, $255d
    push hl
    ld hl, $0303
    push hl
    ld a, c
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4fe3
    add sp, $06

Jump_000_26d2:
    ld hl, sp+$06
    ld a, [hl]
    cp $04
    jp nz, Jump_000_26de

    ld a, $01
    jr jr_000_26df

Jump_000_26de:
    xor a

jr_000_26df:
    ld c, a
    xor a
    or c
    jp nz, Jump_000_26f2

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_2712

    jr jr_000_26f2

    jp Jump_000_2712


Jump_000_26f2:
jr_000_26f2:
    ld hl, sp+$07
    ld a, [hl]
    or a
    jp nz, Jump_000_2712

    jr jr_000_26fe

    jp Jump_000_2712


jr_000_26fe:
    push bc
    ld hl, $2566
    push hl
    ld hl, $0306
    push hl
    ld hl, $050e
    push hl
    call $4fe3
    add sp, $06
    pop hl
    ld c, l

Jump_000_2712:
    xor a
    or c
    jp nz, Jump_000_2724

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_2745

    jr jr_000_2724

    jp Jump_000_2745


Jump_000_2724:
jr_000_2724:
    ld hl, sp+$07
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2745

    jr jr_000_2731

    jp Jump_000_2745


jr_000_2731:
    push bc
    ld hl, $2566
    push hl
    ld hl, $0306
    push hl
    ld hl, $080e
    push hl
    call $4fe3
    add sp, $06
    pop hl
    ld c, l

Jump_000_2745:
    xor a
    or c
    jp nz, Jump_000_2757

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_2775

    jr jr_000_2757

    jp Jump_000_2775


Jump_000_2757:
jr_000_2757:
    ld hl, sp+$07
    ld a, [hl]
    cp $03
    jp nz, Jump_000_2775

    jr jr_000_2764

    jp Jump_000_2775


jr_000_2764:
    ld hl, $2566
    push hl
    ld hl, $0306
    push hl
    ld hl, $0e0e
    push hl
    call $4fe3
    add sp, $06

Jump_000_2775:
    add sp, $04
    ret


Call_000_2778:
    add sp, -$04
    ld a, $03
    ld hl, sp+$06
    sub [hl]
    jp c, Jump_000_27c9

    ld a, $03
    inc hl
    sub [hl]
    jp c, Jump_000_27c9

    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    ld c, l
    ld b, h
    inc bc
    inc bc
    inc bc
    inc bc
    inc bc
    ld hl, sp+$06
    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0001
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld b, [hl]
    ld hl, $2542
    push hl
    ld hl, $0303
    push hl
    ld a, c
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4fe3
    add sp, $06

Jump_000_27c9:
    ld hl, sp+$06
    ld a, [hl]
    cp $04
    jp nz, Jump_000_27d5

    ld a, $01
    jr jr_000_27d6

Jump_000_27d5:
    xor a

jr_000_27d6:
    ld c, a
    xor a
    or c
    jp nz, Jump_000_27e9

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_2809

    jr jr_000_27e9

    jp Jump_000_2809


Jump_000_27e9:
jr_000_27e9:
    ld hl, sp+$07
    ld a, [hl]
    or a
    jp nz, Jump_000_2809

    jr jr_000_27f5

    jp Jump_000_2809


jr_000_27f5:
    push bc
    ld hl, $254b
    push hl
    ld hl, $0306
    push hl
    ld hl, $050e
    push hl
    call $4fe3
    add sp, $06
    pop hl
    ld c, l

Jump_000_2809:
    xor a
    or c
    jp nz, Jump_000_281b

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_283c

    jr jr_000_281b

    jp Jump_000_283c


Jump_000_281b:
jr_000_281b:
    ld hl, sp+$07
    ld a, [hl]
    cp $01
    jp nz, Jump_000_283c

    jr jr_000_2828

    jp Jump_000_283c


jr_000_2828:
    push bc
    ld hl, $254b
    push hl
    ld hl, $0306
    push hl
    ld hl, $080e
    push hl
    call $4fe3
    add sp, $06
    pop hl
    ld c, l

Jump_000_283c:
    xor a
    or c
    jp nz, Jump_000_284e

    ld hl, sp+$06
    ld a, [hl]
    cp $05
    jp nz, Jump_000_286c

    jr jr_000_284e

    jp Jump_000_286c


Jump_000_284e:
jr_000_284e:
    ld hl, sp+$07
    ld a, [hl]
    cp $03
    jp nz, Jump_000_286c

    jr jr_000_285b

    jp Jump_000_286c


jr_000_285b:
    ld hl, $254b
    push hl
    ld hl, $0306
    push hl
    ld hl, $0e0e
    push hl
    call $4fe3
    add sp, $06

Jump_000_286c:
    add sp, $04
    ret


Call_000_286f:
    add sp, -$07
    ld hl, $c570
    push hl
    ld hl, $1800
    push hl
    call $4f37
    add sp, $04
    ld hl, sp+$04
    ld [hl], $01

Jump_000_2882:
    ld a, $03
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_28c4

    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, sp+$06
    ld [hl-], a
    dec hl
    ld a, [hl]
    push af
    inc sp
    ld a, [hl]
    push af
    inc sp
    call $4f73
    add sp, $02
    ld a, $40
    push af
    inc sp
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    dec hl
    dec hl
    ld a, [hl]
    push af
    inc sp
    call $4edd
    add sp, $03
    ld hl, sp+$04
    inc [hl]
    jp Jump_000_2882


Jump_000_28c4:
    ld hl, sp+$04
    ld [hl], $04

Jump_000_28c8:
    ld a, $06
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_2909

    ld a, [hl]
    add $fd
    ld b, a
    ld e, b
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld b, l
    ld c, h
    ld hl, sp+$06
    ld [hl], b
    dec hl
    dec hl
    ld a, [hl]
    push af
    inc sp
    ld a, [hl]
    push af
    inc sp
    call $4f73
    add sp, $02
    ld a, $58
    push af
    inc sp
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    dec hl
    dec hl
    ld a, [hl]
    push af
    inc sp
    call $4edd
    add sp, $03
    ld hl, sp+$04
    inc [hl]
    jp Jump_000_28c8


Jump_000_2909:
    ld hl, sp+$04
    ld [hl], $07

Jump_000_290d:
    ld a, $09
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_294e

    ld a, [hl]
    add $fa
    ld c, a
    ld e, c
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld c, l
    ld b, h
    ld hl, sp+$06
    ld [hl], c
    dec hl
    dec hl
    ld a, [hl]
    push af
    inc sp
    ld a, [hl]
    push af
    inc sp
    call $4f73
    add sp, $02
    ld a, $70
    push af
    inc sp
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    dec hl
    dec hl
    ld a, [hl]
    push af
    inc sp
    call $4edd
    add sp, $03
    ld hl, sp+$04
    inc [hl]
    jp Jump_000_290d


Jump_000_294e:
    ld hl, sp+$04
    ld [hl], $00

Jump_000_2952:
    ld a, $03
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_29af

    ld c, [hl]
    inc c
    ld e, c
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0028
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, sp+$05
    ld [hl-], a
    ld a, [hl]
    add $0a
    ld hl, sp+$00
    ld [hl], a
    push bc
    ld a, [hl]
    push af
    inc sp
    ld a, [hl]
    push af
    inc sp
    call $4f73
    add sp, $02
    pop hl
    ld c, l
    push bc
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    ld a, $60
    push af
    inc sp
    ld hl, sp+$04
    ld a, [hl]
    push af
    inc sp
    call $4edd
    add sp, $03
    pop hl
    ld c, l
    ld hl, sp+$04
    ld [hl], c
    jp Jump_000_2952


Jump_000_29af:
    ld hl, $0000
    push hl
    call $4f73
    add sp, $02
    ld hl, $8830
    push hl
    ld a, $00
    push af
    inc sp
    call $4edd
    add sp, $03
    ld hl, sp+$04
    ld [hl], $00

Jump_000_29c9:
    ld a, $02
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_2a21

    ld c, [hl]
    inc c
    ld e, c
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0028
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, sp+$05
    ld [hl-], a
    ld a, [hl]
    add $10
    ld b, a
    push bc
    ld a, b
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4f73
    add sp, $02
    pop bc
    push bc
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    ld a, $80
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4edd
    add sp, $03
    pop hl
    ld c, l
    ld hl, sp+$04
    ld [hl], c
    jp Jump_000_29c9


Jump_000_2a21:
    ld hl, sp+$04
    ld [hl], $00

Jump_000_2a25:
    ld a, $02
    ld hl, sp+$04
    sub [hl]
    jp c, Jump_000_2a7d

    ld c, [hl]
    inc c
    ld e, c
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$00
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0028
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$02
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, sp+$05
    ld [hl-], a
    ld a, [hl]
    add $13
    ld b, a
    push bc
    ld a, b
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4f73
    add sp, $02
    pop bc
    push bc
    ld hl, sp+$07
    ld a, [hl]
    push af
    inc sp
    ld a, $8a
    push af
    inc sp
    ld a, b
    push af
    inc sp
    call $4edd
    add sp, $03
    pop hl
    ld c, l
    ld hl, sp+$04
    ld [hl], c
    jp Jump_000_2a25


Jump_000_2a7d:
    ld hl, $1616
    push hl
    call $4f73
    add sp, $02
    ld hl, $888a
    push hl
    ld a, $16
    push af
    inc sp
    call $4edd
    add sp, $03
    add sp, $07
    ret


Call_000_2a96:
    ld hl, $c0a0
    push hl
    ld hl, $0900
    push hl
    call $4eea
    add sp, $04
    ld hl, $c130
    push hl
    ld hl, $0909
    push hl
    call $4eea
    add sp, $04
    ld hl, $c1c0
    push hl
    ld hl, $0912
    push hl
    call $4eea
    add sp, $04
    ld hl, $23da
    push hl
    ld hl, $1214
    push hl
    ld hl, $0000
    push hl
    call $4fe3
    add sp, $06
    ret


Call_000_2acf:
    ld hl, $c6e0
    push hl
    ld hl, $0817
    push hl
    call $4f37
    add sp, $04
    ld c, $17

Jump_000_2ade:
    ld a, $1e
    sub c
    jp c, Jump_000_2af6

    push bc
    ld a, c
    push af
    inc sp
    ld a, c
    push af
    inc sp
    call $4f73
    add sp, $02
    pop hl
    ld c, l
    inc c
    jp Jump_000_2ade


Jump_000_2af6:
    ret


Call_000_2af7:
    ld hl, sp+$03
    ld a, [hl]
    push af
    inc sp
    dec hl
    ld a, [hl]
    push af
    inc sp
    ld a, $17
    push af
    inc sp
    call $4edd
    add sp, $03
    ld hl, sp+$03
    ld a, [hl]
    add $08
    ld c, a
    push bc
    ld a, c
    push af
    inc sp
    dec hl
    ld a, [hl]
    push af
    inc sp
    ld a, $18
    push af
    inc sp
    call $4edd
    add sp, $03
    pop hl
    ld c, l
    ld hl, sp+$02
    ld a, [hl]
    add $08
    ld b, a
    push bc
    inc hl
    ld a, [hl]
    push af
    inc sp
    ld a, b
    push af
    inc sp
    ld a, $19
    push af
    inc sp
    call $4edd
    add sp, $03
    pop bc
    ld a, c
    push af
    inc sp
    ld a, b
    push af
    inc sp
    ld a, $1a
    push af
    inc sp
    call $4edd
    add sp, $03
    ret


Call_000_2b4a:
    ld hl, $c779
    ld a, [hl]
    or a
    jp nz, Jump_000_2b5f

    jr jr_000_2b57

    jp Jump_000_2b5f


jr_000_2b57:
    ld hl, $c77a
    ld [hl], $01
    jp Jump_000_2bbf


Jump_000_2b5f:
    ld hl, $c779
    ld a, [hl]
    cp $02
    jp z, Jump_000_2bb5

    ld hl, $c779
    ld a, [hl]
    cp $04
    jp z, Jump_000_2b9a

    ld hl, $c779
    ld a, [hl]
    cp $06
    jp z, Jump_000_2ba3

    ld hl, $c779
    ld a, [hl]
    cp $08
    jp z, Jump_000_2bac

    ld hl, $c779
    ld a, [hl]
    cp $0a
    jp z, Jump_000_2ba3

    ld hl, $c779
    ld a, [hl]
    cp $0c
    jp nz, Jump_000_2bbb

    jr jr_000_2b9a

    jp Jump_000_2bbb


Jump_000_2b9a:
jr_000_2b9a:
    ld bc, $ff47
    ld a, $f9
    ld [bc], a
    jp Jump_000_2bbb


Jump_000_2ba3:
    ld bc, $ff47
    ld a, $fe
    ld [bc], a
    jp Jump_000_2bbb


Jump_000_2bac:
    ld bc, $ff47
    ld a, $ff
    ld [bc], a
    jp Jump_000_2bbb


Jump_000_2bb5:
    ld bc, $ff47
    ld a, $e4
    ld [bc], a

Jump_000_2bbb:
    ld hl, $c779
    dec [hl]

Jump_000_2bbf:
    ret


Call_000_2bc0:
    add sp, -$05
    call $48b3
    call $4853
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fd
    ld [bc], a
    ld hl, $03fc
    push hl
    ld hl, $ff00
    push hl
    call $4eea
    add sp, $04
    ld bc, $ff4f
    ld a, $01
    ld [bc], a
    ld bc, $ff4f
    ld a, $00
    ld [bc], a
    ld hl, $0294
    push hl
    ld hl, $1214
    push hl
    ld hl, $0000
    push hl
    call $4fe3
    add sp, $06
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fe
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    or $80
    ld [bc], a
    ld bc, $ff47
    inc hl
    ld [hl], $48
    inc hl
    ld [hl], $ff
    ld hl, sp+$00
    ld [hl], $49
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    inc hl
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    ld a, $e4
    ld [bc], a
    ld hl, $c779
    ld [hl], $0c
    ld hl, $c77a
    ld [hl], $00

Jump_000_2c5c:
    ld c, $00

Jump_000_2c5e:
    ld a, c
    cp $02
    ld a, $00
    rla
    ld b, a
    xor a
    or b
    jp z, Jump_000_2c79

    push bc
    call $483c
    pop bc
    ld a, c
    add $01
    ld hl, sp+$00
    ld [hl], a
    ld c, a
    jp Jump_000_2c5e


Jump_000_2c79:
    ld hl, $c778
    inc [hl]
    call Call_000_2b4a
    ld hl, $c77a
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2c5c

    jr jr_000_2c8e

    jp Jump_000_2c5c


jr_000_2c8e:
    ld bc, $ff40
    ld hl, sp+$00
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    inc hl
    ld [hl], a
    or $01
    ld [bc], a
    call $48b1
    ld a, $b0
    push af
    inc sp
    call $4ec4
    add sp, $01
    add sp, $05
    ret


Call_000_2cb1:
    add sp, -$05
    call $48b3
    call $4853
    ld hl, $0fde
    push hl
    ld hl, $ff00
    push hl
    call $4eea
    add sp, $04
    ld bc, $ff4f
    ld a, $01
    ld [bc], a
    ld bc, $ff4f
    ld a, $00
    ld [bc], a
    ld hl, $0e76
    push hl
    ld hl, $1214
    push hl
    ld hl, $0000
    push hl
    call $4fe3
    add sp, $06
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fe
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    or $80
    ld [bc], a
    ld bc, $ff47
    inc hl
    ld [hl], $48
    inc hl
    ld [hl], $ff
    ld hl, sp+$00
    ld [hl], $49
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    inc hl
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    ld a, $e4
    ld [bc], a
    ld hl, $c779
    ld [hl], $0c
    ld hl, $c77a
    ld [hl], $00

Jump_000_2d38:
    ld c, $00

Jump_000_2d3a:
    ld a, c
    cp $02
    ld a, $00
    rla
    ld b, a
    xor a
    or b
    jp z, Jump_000_2d55

    push bc
    call $483c
    pop bc
    ld a, c
    add $01
    ld hl, sp+$00
    ld [hl], a
    ld c, a
    jp Jump_000_2d3a


Jump_000_2d55:
    ld hl, $c778
    inc [hl]
    call Call_000_2b4a
    ld hl, $c77a
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2d38

    jr jr_000_2d6a

    jp Jump_000_2d38


jr_000_2d6a:
    ld bc, $ff40
    ld hl, sp+$00
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    inc hl
    ld [hl], a
    or $01
    ld [bc], a
    call $48b1
    ld a, $b0
    push af
    inc sp
    call $4ec4
    add sp, $01
    add sp, $05
    ret


Call_000_2d8d:
    add sp, -$05
    call $48b3
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fe
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    or $80
    ld [bc], a
    ld bc, $ff47
    inc hl
    ld [hl], $48
    inc hl
    ld [hl], $ff
    ld hl, sp+$00
    ld [hl], $49
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    inc hl
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    ld a, $e4
    ld [bc], a
    ld hl, $c779
    ld [hl], $0c
    ld hl, $c77a
    ld [hl], $00

Jump_000_2de7:
    ld c, $00

Jump_000_2de9:
    ld a, c
    cp $02
    ld a, $00
    rla
    ld b, a
    xor a
    or b
    jp z, Jump_000_2e04

    push bc
    call $483c
    pop bc
    ld a, c
    add $01
    ld hl, sp+$00
    ld [hl], a
    ld c, a
    jp Jump_000_2de9


Jump_000_2e04:
    ld hl, $c778
    inc [hl]
    call Call_000_2b4a
    ld hl, $c77a
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2de7

    jr jr_000_2e19

    jp Jump_000_2de7


jr_000_2e19:
    ld bc, $ff40
    ld hl, sp+$00
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    inc hl
    ld [hl], a
    or $01
    ld [bc], a
    call $48b1
    add sp, $05
    ret


    add sp, -$05
    call $48b3
    call $4853
    ld hl, $1f2a
    push hl
    ld hl, $ff00
    push hl
    call $4eea
    add sp, $04
    ld bc, $ff4f
    ld a, $01
    ld [bc], a
    ld bc, $ff4f
    ld a, $00
    ld [bc], a
    ld hl, $1b2a
    push hl
    ld hl, $2020
    push hl
    ld hl, $0000
    push hl
    call $4fe3
    add sp, $06
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fd
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fe
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    or $80
    ld [bc], a
    ld bc, $ff47
    inc hl
    ld [hl], $48
    inc hl
    ld [hl], $ff
    ld hl, sp+$00
    ld [hl], $49
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    inc hl
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    ld a, $e4
    ld [bc], a
    ld hl, $c779
    ld [hl], $0c
    ld hl, $c77a
    ld [hl], $00

Jump_000_2ece:
    ld c, $00

Jump_000_2ed0:
    ld a, c
    cp $02
    ld a, $00
    rla
    ld b, a
    xor a
    or b
    jp z, Jump_000_2eeb

    push bc
    call $483c
    pop bc
    ld a, c
    add $01
    ld hl, sp+$00
    ld [hl], a
    ld c, a
    jp Jump_000_2ed0


Jump_000_2eeb:
    ld hl, $c778
    inc [hl]
    call Call_000_2b4a
    ld hl, $c77a
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2ece

    jr jr_000_2f00

    jp Jump_000_2ece


jr_000_2f00:
    ld bc, $ff40
    ld hl, sp+$00
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    inc hl
    ld [hl], a
    or $01
    ld [bc], a
    ld hl, $4e20
    push hl
    call $4fb8
    add sp, $02
    add sp, $05
    ret


Call_000_2f20:
    add sp, -$05
    call $48b3
    call $4853
    ld hl, $18c0
    push hl
    ld hl, $ff00
    push hl
    call $4eea
    add sp, $04
    ld bc, $ff4f
    ld a, $01
    ld [bc], a
    ld bc, $ff4f
    ld a, $00
    ld [bc], a
    ld hl, $1758
    push hl
    ld hl, $1214
    push hl
    ld hl, $0000
    push hl
    call $4fe3
    add sp, $06
    ld bc, $ff40
    ld hl, sp+$03
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fd
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    and $fe
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    or $80
    ld [bc], a
    ld bc, $ff47
    inc hl
    ld [hl], $48
    inc hl
    ld [hl], $ff
    ld hl, sp+$00
    ld [hl], $49
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    inc hl
    inc hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $e4
    ld [de], a
    ld a, $e4
    ld [bc], a
    ld hl, $c779
    ld [hl], $0c
    ld hl, $c77a
    ld [hl], $00

Jump_000_2fbb:
    ld c, $00

Jump_000_2fbd:
    ld a, c
    cp $02
    ld a, $00
    rla
    ld b, a
    xor a
    or b
    jp z, Jump_000_2fd8

    push bc
    call $483c
    pop bc
    ld a, c
    add $01
    ld hl, sp+$00
    ld [hl], a
    ld c, a
    jp Jump_000_2fbd


Jump_000_2fd8:
    ld hl, $c778
    inc [hl]
    call Call_000_2b4a
    ld hl, $c77a
    ld a, [hl]
    cp $01
    jp nz, Jump_000_2fbb

    jr jr_000_2fed

    jp Jump_000_2fbb


jr_000_2fed:
    ld bc, $ff40
    ld hl, sp+$00
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    inc hl
    ld [hl], a
    or $01
    ld [bc], a
    ld hl, $01f4
    push hl
    call $4fb8
    add sp, $02
    add sp, $05
    ret


Call_000_300d:
    add sp, -$03
    ld bc, $ff40
    ld hl, sp+$01
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    ld a, a
    and $fd
    ld [bc], a
    ld hl, $303d
    push hl
    call $4ba1
    add sp, $02

Jump_000_302e:
    ld hl, $03e8
    push hl
    call $4fb8
    add sp, $02
    jp Jump_000_302e


    add sp, $03
    ret


    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl+]
    jr nz, jr_000_30b5

    ld [hl], h
    ld h, c
    ld h, e
    ld l, e
    jr nz, jr_000_30bb

    ld l, l
    ld h, c
    ld [hl], e
    ld l, b
    ld l, c
    ld l, [hl]
    ld h, a
    jr nz, jr_000_30b5

    ld h, l
    ld [hl], h
    ld h, l
    ld h, e
    ld [hl], h
    ld h, l
    ld h, h
    jr nz, jr_000_3084

    ld a, [hl+]
    ld a, [hl+]
    ld a, [hl-]
    jr nz, jr_000_309b

    ld [hl], l
    ld l, [hl]
    ld l, e
    ld l, [hl]
    ld l, a
    ld [hl], a
    ld l, [hl]
    ld a, $20
    ld [hl], h
    ld h, l
    ld [hl], d
    ld l, l
    ld l, c
    ld l, [hl]
    ld h, c
    ld [hl], h
    ld h, l
    ld h, h
    ld a, [bc]
    ld b, c
    ld h, d
    ld l, a
    ld [hl], d
    ld [hl], h
    ld h, l
    ld h, h
    nop

Call_000_307b:
    add sp, -$1e
    ld hl, $c784
    ld a, [hl+]
    ld e, [hl]
    ld hl, sp+$1c

jr_000_3084:
    ld [hl+], a
    ld [hl], e
    ld hl, sp+$0c
    ld c, l
    ld b, h
    ld hl, sp+$0a
    ld [hl], c
    inc hl
    ld [hl], b
    push bc
    dec hl
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    call $4960
    ldh a, [rP1]
    nop
    pop bc

jr_000_309b:
    ld hl, $c79f
    ld [hl], $00
    ld hl, $c7a1
    ld [hl], $00
    ld hl, $c7a0
    ld [hl], $00
    ld hl, $c7a4
    ld [hl], $00

Jump_000_30af:
    push bc
    call $483c
    pop bc
    push bc

jr_000_30b5:
    call $4ebf
    ld hl, $c79e

jr_000_30bb:
    ld [hl], e
    pop bc
    ld hl, $c79f
    ld a, [hl]
    ld hl, $c79e
    cp [hl]
    jr nz, jr_000_30ca

    jp Jump_000_3128


jr_000_30ca:
    ld hl, $c7a0
    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$0a
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0018
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$08
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, $c7a2
    ld [hl], a
    ld hl, $c7a1
    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, l
    ld d, h
    ld hl, sp+$08
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $0048
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$0a
    ld [hl+], a
    ld [hl], d
    dec hl
    ld a, [hl]
    ld hl, $c7a3
    ld [hl], a
    push bc
    ld a, [hl]
    push af
    inc sp
    ld hl, $c7a2
    ld a, [hl]
    push af
    inc sp
    call Call_000_2af7
    add sp, $02
    pop bc

Jump_000_3128:
    ld hl, $c79f
    ld a, [hl]
    and $10
    jr nz, jr_000_3133

    jp Jump_000_3157


jr_000_3133:
    ld hl, $c79e
    ld a, [hl]
    and $10
    jr nz, jr_000_313e

    jp Jump_000_3141


jr_000_313e:
    jp Jump_000_34bc


Jump_000_3141:
    push bc
    ld hl, $c7a1
    ld a, [hl]
    push af
    inc sp
    ld hl, $c7a0
    ld a, [hl]
    push af
    inc sp
    call Call_000_2778
    add sp, $02
    pop bc
    jp Jump_000_34bc


Jump_000_3157:
    ld hl, $c79e
    ld a, [hl]
    and $10
    jr nz, jr_000_3162

    jp Jump_000_34bc


jr_000_3162:
    push bc
    ld hl, $c7a1
    ld a, [hl]
    push af
    inc sp
    ld hl, $c7a0
    ld a, [hl]
    push af
    inc sp
    call Call_000_2681
    add sp, $02
    pop bc
    ld a, $02
    ld hl, $c7a0
    sub [hl]
    jp c, Jump_000_3234

    ld a, $03
    ld hl, $c7a1
    sub [hl]
    jp c, Jump_000_3234

    ld e, $80
    ld hl, $c783
    ld a, [hl]
    xor $80
    ld d, a
    ld a, $00
    dec hl
    sub [hl]
    ld a, e
    sbc d
    jp nc, Jump_000_31ba

    ld hl, $c7a4
    ld [hl], $00
    push bc
    ld hl, $3621
    push hl
    ld hl, $c786
    push hl
    call $4987
    add sp, $04
    pop bc
    push bc
    call $25a8
    pop bc
    ld hl, $c782
    ld [hl], $00
    inc hl
    ld [hl], $00

Jump_000_31ba:
    ld hl, $c7a4
    ld a, [hl]
    cp $12
    jp nc, Jump_000_3234

    ld de, $c786
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$08
    ld [hl+], a
    ld [hl], d
    ld hl, $c7a1
    ld e, [hl]
    ld d, $00
    ld l, e
    ld h, d
    add hl, hl
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$0a
    ld [hl+], a
    ld [hl], d
    ld de, $259c
    dec hl
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$06
    ld [hl+], a
    ld [hl], d
    ld hl, $c7a0
    ld a, [hl]
    ld e, $00
    ld hl, sp+$0a
    ld [hl+], a
    ld [hl], e
    ld hl, sp+$06
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, sp+$0a
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$04
    ld [hl+], a
    ld [hl], d
    ld e, a
    ld a, [de]
    ld hl, sp+$08
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld [de], a
    ld hl, $c7a4
    inc [hl]
    ld de, $c786
    ld l, [hl]
    ld h, $00
    add hl, de
    ld a, l
    ld d, h
    ld hl, sp+$04
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, $00
    ld [de], a
    push bc
    ld hl, $c786
    push hl
    call Call_000_25c7
    add sp, $02
    pop bc

Jump_000_3234:
    ld hl, $c7a0
    ld a, [hl]
    cp $04
    ld a, $00
    rla
    ld hl, sp+$04
    ld [hl], a
    xor a
    or [hl]
    jp nz, Jump_000_3285

    ld hl, $c7a1
    ld a, [hl]
    or a
    jp nz, Jump_000_3285

    jr jr_000_3252

    jp Jump_000_3285


jr_000_3252:
    ld hl, $c7a4
    ld [hl], $00
    push bc
    ld hl, $3622
    push hl
    ld hl, $c786
    push hl
    call $4987
    add sp, $04
    pop bc
    push bc
    call $25a8
    pop bc
    ld hl, $c782
    ld [hl], $00
    inc hl
    ld [hl], $00
    ld hl, $c780
    ld [hl], $00
    inc hl
    ld [hl], $00
    ld hl, $c7a6
    ld [hl], $00
    ld hl, $c7a7
    ld [hl], $00

Jump_000_3285:
    xor a
    ld hl, sp+$04
    or [hl]
    jp nz, Jump_000_32bc

    ld hl, $c7a1
    ld a, [hl]
    cp $01
    jp nz, Jump_000_32bc

    jr jr_000_329a

    jp Jump_000_32bc


jr_000_329a:
    push bc
    call $25a8
    pop bc
    ld hl, $c784
    ld a, [hl]
    ld hl, sp+$1c
    cp [hl]
    jr nz, jr_000_32b4

    ld hl, $c785
    ld a, [hl]
    ld hl, sp+$1d
    cp [hl]
    jr nz, jr_000_32b4

    jp Jump_000_32b9


jr_000_32b4:
    push bc
    call Call_000_300d
    pop bc

Jump_000_32b9:
    jp Jump_000_361e


Jump_000_32bc:
    ld hl, $c7a0
    ld a, [hl]
    cp $03
    jp nz, Jump_000_32c9

    ld a, $01
    jr jr_000_32ca

Jump_000_32c9:
    xor a

jr_000_32ca:
    ld hl, sp+$06
    ld [hl], a
    xor a
    or [hl]
    jp z, Jump_000_32e4

    ld hl, $c7a1
    ld a, [hl]
    or a
    jp nz, Jump_000_32e4

    jr jr_000_32df

    jp Jump_000_32e4


jr_000_32df:
    ld hl, $c7a7
    ld [hl], $01

Jump_000_32e4:
    xor a
    ld hl, sp+$06
    or [hl]
    jp z, Jump_000_32fe

    ld hl, $c7a1
    ld a, [hl]
    cp $01
    jp nz, Jump_000_32fe

    jr jr_000_32f9

    jp Jump_000_32fe


jr_000_32f9:
    ld hl, $c7a7
    ld [hl], $02

Jump_000_32fe:
    xor a
    ld hl, sp+$06
    or [hl]
    jp z, Jump_000_3318

    ld hl, $c7a1
    ld a, [hl]
    cp $02
    jp nz, Jump_000_3318

    jr jr_000_3313

    jp Jump_000_3318


jr_000_3313:
    ld hl, $c7a7
    ld [hl], $03

Jump_000_3318:
    xor a
    ld hl, sp+$06
    or [hl]
    jp z, Jump_000_3332

    ld hl, $c7a1
    ld a, [hl]
    cp $03
    jp nz, Jump_000_3332

    jr jr_000_332d

    jp Jump_000_3332


jr_000_332d:
    ld hl, $c7a7
    ld [hl], $04

Jump_000_3332:
    xor a
    ld hl, sp+$04
    or [hl]
    jp nz, Jump_000_334c

    ld hl, $c7a1
    ld a, [hl]
    cp $03
    jp nz, Jump_000_334c

    jr jr_000_3347

    jp Jump_000_334c


jr_000_3347:
    ld hl, $c7a7
    ld [hl], $05

Jump_000_334c:
    ld a, $00
    ld hl, $c7a7
    sub [hl]
    jp nc, Jump_000_34bc

    ld hl, $c782
    ld [hl], $00
    inc hl
    ld [hl], $00
    push bc
    ld hl, $c786
    push hl
    call $4a57
    push hl
    ld hl, sp+$06
    ld [hl], e
    inc hl
    ld [hl], d
    pop de
    inc hl
    ld [hl], e
    inc hl
    ld [hl], d
    add sp, $02
    pop bc
    ld hl, sp+$00
    ld a, [hl]
    ld hl, $c782
    ld [hl], a
    ld hl, sp+$01
    ld a, [hl]
    ld hl, $c783
    ld [hl], a
    ld hl, $c7a6
    ld a, [hl]
    cp $01
    jp c, Jump_000_3415

    ld a, $04
    sub [hl]
    jp c, Jump_000_3415

    ld a, [hl]
    add $ff
    ld hl, sp+$00
    ld [hl], a
    ld e, a
    ld d, $00
    ld hl, $33a0
    add hl, de
    add hl, de
    add hl, de
    jp hl


    jp Jump_000_33ac


    jp Jump_000_33c4


    jp Jump_000_33dc


    jp Jump_000_33fa


Jump_000_33ac:
    ld hl, $c780
    ld a, [hl]
    ld hl, $c782
    add [hl]
    ld hl, $c780
    ld [hl+], a
    ld a, [hl]
    ld hl, $c783
    adc [hl]
    ld hl, $c781
    ld [hl], a
    jp Jump_000_3415


Jump_000_33c4:
    ld hl, $c780
    ld a, [hl]
    ld hl, $c782
    sub [hl]
    ld hl, $c780
    ld [hl+], a
    ld a, [hl]
    ld hl, $c783
    sbc [hl]
    ld hl, $c781
    ld [hl], a
    jp Jump_000_3415


Jump_000_33dc:
    push bc
    ld hl, $c782
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    push hl
    ld hl, $c780
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    push hl
    call Call_000_37d0
    ld hl, $c781
    ld [hl], d
    dec hl
    ld [hl], e
    add sp, $04
    pop bc
    jp Jump_000_3415


Jump_000_33fa:
    push bc
    ld hl, $c782
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    push hl
    ld hl, $c780
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    push hl
    call Call_000_36c8
    ld hl, $c781
    ld [hl], d
    dec hl
    ld [hl], e
    add sp, $04
    pop bc

Jump_000_3415:
    ld hl, $c7a6
    ld a, [hl]
    or a
    jp nz, Jump_000_3445

    jr jr_000_3422

    jp Jump_000_3445


jr_000_3422:
    ld hl, $c7a4
    ld [hl], $00
    push bc
    ld hl, $3623
    push hl
    ld hl, $c786
    push hl
    call $4987
    add sp, $04
    pop bc
    push bc
    call $25a8
    pop bc
    ld hl, $c782
    ld a, [hl+]
    ld e, [hl]
    ld hl, $c780
    ld [hl+], a
    ld [hl], e

Jump_000_3445:
    push bc
    ld hl, $c780
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    push hl
    ld hl, $3624
    push hl
    ld hl, $c786
    push hl
    call $4bbe
    add sp, $06
    pop bc
    push bc
    ld hl, $c786
    push hl
    call Call_000_25c7
    add sp, $02
    pop bc
    ld hl, $c7a7
    ld a, [hl]
    cp $05
    jp nz, Jump_000_34af

    jr jr_000_3474

    jp Jump_000_34af


jr_000_3474:
    ld hl, $c7a5
    ld a, [hl]
    ld hl, sp+$00
    ld [hl], a
    ld hl, $c7a5
    inc [hl]
    ld hl, sp+$00
    ld a, [hl]
    ld hl, sp+$04
    ld [hl+], a
    ld [hl], $00
    dec hl
    ld a, [hl]
    ld hl, sp+$00
    ld [hl], a
    ld hl, sp+$05
    ld a, [hl]
    ld hl, sp+$01
    ld [hl-], a
    sla [hl]
    inc hl
    rl [hl]
    dec hl
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    add hl, bc
    ld a, l
    ld d, h
    ld hl, sp+$04
    ld [hl+], a
    ld [hl], d
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld hl, $c780
    ld a, [hl]
    ld [de], a
    inc de
    inc hl
    ld a, [hl]
    ld [de], a

Jump_000_34af:
    ld hl, $c7a7
    ld a, [hl]
    ld hl, $c7a6
    ld [hl], a
    ld hl, $c7a7
    ld [hl], $00

Jump_000_34bc:
    ld hl, $c79e
    ld a, [hl]
    and $10
    jr nz, jr_000_34c7

    jp Jump_000_34ca


jr_000_34c7:
    jp Jump_000_3613


Jump_000_34ca:
    ld hl, $c79e
    ld a, [hl]
    and $04
    jr nz, jr_000_34d5

    jp Jump_000_350d


jr_000_34d5:
    ld hl, $c79f
    ld a, [hl]
    and $04
    jr nz, jr_000_34e0

    jp Jump_000_34e3


jr_000_34e0:
    jp Jump_000_350d


Jump_000_34e3:
    ld a, $00
    ld hl, $c7a1
    sub [hl]
    jp nc, Jump_000_350d

    dec [hl]
    ld a, [hl]
    cp $02
    jp nz, Jump_000_354d

    jr jr_000_34f8

    jp Jump_000_354d


jr_000_34f8:
    ld hl, $c7a0
    ld a, [hl]
    cp $05
    jp nz, Jump_000_354d

    jr jr_000_3506

    jp Jump_000_354d


jr_000_3506:
    ld hl, $c7a1
    dec [hl]
    jp Jump_000_354d


Jump_000_350d:
    ld hl, $c79e
    ld a, [hl]
    and $08
    jr nz, jr_000_3518

    jp Jump_000_354d


jr_000_3518:
    ld hl, $c79f
    ld a, [hl]
    and $08
    jr nz, jr_000_3523

    jp Jump_000_3526


jr_000_3523:
    jp Jump_000_354d


Jump_000_3526:
    ld hl, $c7a1
    ld a, [hl]
    cp $03
    jp nc, Jump_000_354d

    inc [hl]
    ld a, [hl]
    cp $02
    jp nz, Jump_000_354d

    jr jr_000_353b

    jp Jump_000_354d


jr_000_353b:
    ld hl, $c7a0
    ld a, [hl]
    cp $05
    jp nz, Jump_000_354d

    jr jr_000_3549

    jp Jump_000_354d


jr_000_3549:
    ld hl, $c7a1
    inc [hl]

Jump_000_354d:
    ld hl, $c79e
    ld a, [hl]
    and $02
    jr nz, jr_000_3558

    jp Jump_000_3582


jr_000_3558:
    ld hl, $c79f
    ld a, [hl]
    and $02
    jr nz, jr_000_3563

    jp Jump_000_3566


jr_000_3563:
    jp Jump_000_3582


Jump_000_3566:
    ld a, $00
    ld hl, $c7a0
    sub [hl]
    jp nc, Jump_000_3582

    dec [hl]
    ld a, [hl]
    cp $04
    jp nz, Jump_000_35d4

    jr jr_000_357b

    jp Jump_000_35d4


jr_000_357b:
    ld hl, $c7a0
    dec [hl]
    jp Jump_000_35d4


Jump_000_3582:
    ld hl, $c79e
    ld a, [hl]
    and $01
    jr nz, jr_000_358d

    jp Jump_000_35d4


jr_000_358d:
    ld hl, $c79f
    ld a, [hl]
    and $01
    jr nz, jr_000_3598

    jp Jump_000_359b


jr_000_3598:
    jp Jump_000_35d4


Jump_000_359b:
    ld hl, $c7a0
    ld a, [hl]
    cp $05
    jp nc, Jump_000_35d4

    inc [hl]
    ld a, [hl]
    cp $04
    jp nz, Jump_000_35c2

    jr jr_000_35b0

    jp Jump_000_35c2


jr_000_35b0:
    ld hl, $c7a1
    ld a, [hl]
    cp $02
    jp nz, Jump_000_35c2

    jr jr_000_35be

    jp Jump_000_35c2


jr_000_35be:
    ld hl, $c7a0
    dec [hl]

Jump_000_35c2:
    ld hl, $c7a0
    ld a, [hl]
    cp $04
    jp nz, Jump_000_35d4

    jr jr_000_35d0

    jp Jump_000_35d4


jr_000_35d0:
    ld hl, $c7a0
    inc [hl]

Jump_000_35d4:
    ld hl, $c7a0
    ld a, [hl]
    or a
    jp nz, Jump_000_35f3

    jr jr_000_35e1

    jp Jump_000_35f3


jr_000_35e1:
    ld hl, $c7a1
    ld a, [hl]
    cp $03
    jp nz, Jump_000_35f3

    jr jr_000_35ef

    jp Jump_000_35f3


jr_000_35ef:
    ld hl, $c7a1
    dec [hl]

Jump_000_35f3:
    ld hl, $c7a0
    ld a, [hl]
    cp $02
    jp nz, Jump_000_3613

    jr jr_000_3601

    jp Jump_000_3613


jr_000_3601:
    ld hl, $c7a1
    ld a, [hl]
    cp $03
    jp nz, Jump_000_3613

    jr jr_000_360f

    jp Jump_000_3613


jr_000_360f:
    ld hl, $c7a1
    dec [hl]

Jump_000_3613:
    ld hl, $c79e
    ld a, [hl]
    ld hl, $c79f
    ld [hl], a
    jp Jump_000_30af


Jump_000_361e:
    add sp, $1e
    ret


    nop
    nop
    nop
    dec h
    ld [hl], l
    nop
    add sp, -$03
    ld bc, $ff40
    ld hl, sp+$01
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    ld a, a
    and $fb
    ld [bc], a
    call Call_000_2bc0
    call Call_000_2cb1
    call $4e7b
    call $4853
    call Call_000_2a96
    call Call_000_286f
    call Call_000_2acf
    ld hl, $36ac
    push hl
    call Call_000_25c7
    add sp, $02
    call Call_000_2d8d
    ld bc, $ff40
    ld hl, sp+$01
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    ld a, a
    or $01
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    ld a, a
    or $02
    ld [bc], a
    ld bc, $ff40
    inc hl
    ld [hl], $40
    inc hl
    ld [hl], $ff
    dec hl
    ld e, [hl]
    inc hl
    ld d, [hl]
    ld a, [de]
    dec hl
    dec hl
    ld [hl], a
    ld a, a
    or $80
    ld [bc], a
    call $48b1
    call Call_000_307b
    call Call_000_2f20
    add sp, $03
    ret


    jr nc, jr_000_36ae

Jump_000_36ae:
jr_000_36ae:
    ld hl, $0003
    add hl, sp
    ld e, [hl]
    dec hl
    ld l, [hl]
    ld c, l
    call Call_000_372e
    ld e, c
    ld d, b
    ret


Jump_000_36bc:
    ld hl, $0003
    add hl, sp
    ld e, [hl]
    dec hl
    ld l, [hl]
    ld c, l
    call Call_000_372e
    ret


Call_000_36c8:
Jump_000_36c8:
    ld hl, $0005
    add hl, sp
    ld d, [hl]
    dec hl
    ld e, [hl]
    dec hl
    ld a, [hl]
    dec hl
    ld l, [hl]
    ld h, a
    ld b, h
    ld c, l
    call Call_000_3736
    ld e, c
    ld d, b
    ret


Jump_000_36dc:
    ld hl, $0005
    add hl, sp
    ld d, [hl]
    dec hl
    ld e, [hl]
    dec hl
    ld a, [hl]
    dec hl
    ld l, [hl]
    ld h, a
    ld b, h
    ld c, l
    call Call_000_3736
    ret


Jump_000_36ee:
    ld hl, $0003
    add hl, sp
    ld e, [hl]
    dec hl
    ld l, [hl]
    ld c, l
    call Call_000_3770
    ld e, c
    ld d, b
    ret


Jump_000_36fc:
    ld hl, $0003
    add hl, sp
    ld e, [hl]
    dec hl
    ld l, [hl]
    ld c, l
    call Call_000_3770
    ret


Jump_000_3708:
    ld hl, $0005
    add hl, sp
    ld d, [hl]
    dec hl
    ld e, [hl]
    dec hl
    ld a, [hl]
    dec hl
    ld l, [hl]
    ld h, a
    ld b, h
    ld c, l
    call Call_000_3773
    ld e, c
    ld d, b
    ret


Jump_000_371c:
    ld hl, $0005
    add hl, sp
    ld d, [hl]
    dec hl
    ld e, [hl]
    dec hl
    ld a, [hl]
    dec hl
    ld l, [hl]
    ld h, a
    ld b, h
    ld c, l
    call Call_000_3773
    ret


Call_000_372e:
    ld a, c
    rlca
    sbc a
    ld b, a
    ld a, e
    rlca
    sbc a
    ld d, a

Call_000_3736:
    ld a, b
    ld [$c801], a
    xor d
    ld [$c802], a
    bit 7, d
    jr z, jr_000_3748

    sub a
    sub e
    ld e, a
    sbc a
    sub d
    ld d, a

jr_000_3748:
    bit 7, b
    jr z, jr_000_3752

    sub a
    sub c
    ld c, a
    sbc a
    sub b
    ld b, a

jr_000_3752:
    call Call_000_3773
    ret c

    ld a, [$c802]
    and $80
    jr z, jr_000_3763

    sub a
    sub c
    ld c, a
    sbc a
    sub b
    ld b, a

jr_000_3763:
    ld a, [$c801]
    and $80
    ret z

    sub a
    sub e
    ld e, a
    sbc a
    sub d
    ld d, a
    ret


Call_000_3770:
    ld b, $00
    ld d, b

Call_000_3773:
    ld a, e
    or d
    jr nz, jr_000_377e

    ld bc, $0000
    ld d, b
    ld e, c
    scf
    ret


jr_000_377e:
    ld l, c
    ld h, b
    ld bc, $0000
    or a
    ld a, $10

jr_000_3786:
    ld [$c803], a
    rl l
    rl h
    rl c
    rl b
    push bc
    ld a, c
    sbc e
    ld c, a
    ld a, b
    sbc d
    ld b, a
    ccf
    jr c, jr_000_379e

    pop bc
    jr jr_000_37a0

jr_000_379e:
    inc sp
    inc sp

jr_000_37a0:
    ld a, [$c803]
    dec a
    jr nz, jr_000_3786

    ld d, b
    ld e, c
    rl l
    ld c, l
    rl h
    ld b, h
    or a
    ret


Jump_000_37b0:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld l, [hl]
    ld c, l
    ld a, l
    rla
    sbc a
    ld b, a
    ld a, e
    rla
    sbc a
    ld d, a
    jp Jump_000_37de


Jump_000_37c3:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld c, [hl]
    xor a
    ld d, a
    ld b, a
    jp Jump_000_37de


Call_000_37d0:
Jump_000_37d0:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld d, [hl]
    inc hl
    ld a, [hl]
    inc hl
    ld h, [hl]
    ld l, a
    ld b, h
    ld c, l

Jump_000_37de:
    ld hl, $0000
    ld a, b
    ld b, $10
    or a
    jp nz, Jump_000_37eb

    ld b, $08
    ld a, c

Jump_000_37eb:
jr_000_37eb:
    add hl, hl
    rl c
    rla
    jr nc, jr_000_37f2

    add hl, de

jr_000_37f2:
    dec b
    jr nz, jr_000_37eb

    ld e, l
    ld d, h
    ret


    jp $477e


    jp $4432


    jp $404f


    jp $4163


    jp $4253


    jp $4367


    ld a, $05
    rst $08
    jp Jump_000_37d0


    ld a, $05
    rst $08
    jp Jump_000_36c8


    ld a, $05
    rst $08
    jp Jump_000_37d0


    ld a, $05
    rst $08
    jp Jump_000_3708


    ld a, $05
    rst $08
    jp Jump_000_37b0


    ld a, $05
    rst $08
    jp Jump_000_36ae


    ld a, $05
    rst $08
    jp Jump_000_37c3


    ld a, $05
    rst $08
    jp Jump_000_36ee


    ld a, $05
    rst $08
    jp Jump_000_36bc


    ld a, $05
    rst $08
    jp Jump_000_36fc


    ld a, $05
    rst $08
    jp Jump_000_36dc


    ld a, $05
    rst $08
    jp Jump_000_371c


    ld a, $05
    rst $08
    jp Jump_000_386a


    ld a, $05
    rst $08
    jp Jump_000_3887


    ld a, $05
    rst $08
    jp Jump_000_38a4


    ld a, $05
    rst $08
    jp Jump_000_38a4


Jump_000_386a:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld d, [hl]
    inc hl
    ld c, [hl]
    inc hl
    ld b, [hl]
    inc hl
    ld a, [hl]
    ld l, c
    ld h, b

Jump_000_3879:
    or a
    ret z

    rr h
    rr l
    rr d
    rr e
    dec a
    jp Jump_000_3879


Jump_000_3887:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld d, [hl]
    inc hl
    ld c, [hl]
    inc hl
    ld b, [hl]
    inc hl
    ld a, [hl]
    ld l, c
    ld h, b

Jump_000_3896:
    or a
    ret z

    sra h
    rr l
    rr d
    rr e
    dec a
    jp Jump_000_3896


Jump_000_38a4:
    ld hl, $0002
    add hl, sp
    ld e, [hl]
    inc hl
    ld d, [hl]
    inc hl
    ld c, [hl]
    inc hl
    ld b, [hl]
    inc hl
    ld a, [hl]
    ld l, c
    ld h, b

Jump_000_38b3:
    or a
    ret z

    rl e
    rl d
    rl l
    rl h
    dec a
    jp Jump_000_38b3


    ld hl, sp+$02
    ld a, [hl]
    xor $80
    cp $b0
    jp c, Jump_000_38db

    ld e, $b9
    ld a, [hl]
    xor $80
    ld d, a
    ld a, e
    sub d
    jp c, Jump_000_38db

    ld e, $01
    jp Jump_000_38dd


Jump_000_38db:
    ld e, $00

Jump_000_38dd:
    ret


    push bc
    ld hl, sp+$04
    ld a, [hl]
    call $511f
    pop bc
    ret


    push bc
    ld hl, sp+$04
    ld a, [hl]
    call $5148
    pop bc
    ret


    ld hl, sp+$02
    ld a, [hl+]
    ld [$c81a], a
    ld a, [hl]
    ld [$c81b], a
    ret


    ld a, [$c7a9]
    and $02
    jr nz, jr_000_3907

    push bc
    call $527c
    pop bc

jr_000_3907:
    ld a, [$c81a]
    ld e, a
    ret


    ld a, [$c7a9]
    and $02
    jr nz, jr_000_3918

    push bc
    call $527c
    pop bc

jr_000_3918:
    ld a, [$c81b]
    ld e, a
    ret


Call_000_391d:
    push hl
    ld hl, $c82d
    ld a, $13
    cp [hl]
    jr z, jr_000_3929

    inc [hl]
    jr jr_000_3938

jr_000_3929:
    ld [hl], $00
    ld hl, $c82e
    ld a, $11
    cp [hl]
    jr z, jr_000_3936

    inc [hl]
    jr jr_000_3938

jr_000_3936:
    ld [hl], $00

jr_000_3938:
    pop hl
    ret


Call_000_393a:
    ld a, b
    ld [$c820], a
    ld a, c
    ld [$c822], a
    xor a
    ld [$c821], a
    ld a, d
    ld [$c823], a
    cpl
    ld l, a
    ld h, $ff
    inc hl
    ld bc, $0000
    add hl, bc
    ld a, l
    ld [$c828], a
    ld a, h
    ld [$c827], a

Jump_000_395b:
jr_000_395b:
    ld a, [$c821]
    ld b, a
    ld a, [$c823]
    sub b
    ret c

    ld a, [$c81f]
    or a
    call z, Call_000_3a71
    ld a, [$c827]
    bit 7, a
    jr z, jr_000_399f

    ld a, [$c81f]
    or a
    call nz, Call_000_39dd
    ld a, [$c821]
    inc a
    ld [$c821], a
    ld a, [$c827]
    ld b, a
    ld a, [$c828]
    ld c, a
    ld h, $00
    ld a, [$c821]
    ld l, a
    add hl, hl
    add hl, hl
    add hl, bc
    ld bc, $0006
    add hl, bc
    ld a, h
    ld [$c827], a
    ld a, l
    ld [$c828], a
    jr jr_000_395b

jr_000_399f:
    ld a, [$c81f]
    or a
    call nz, Call_000_3a15
    ld a, [$c821]
    inc a
    ld [$c821], a
    ld b, $00
    ld a, [$c821]
    ld c, a
    ld h, $ff
    ld a, [$c823]
    cpl
    ld l, a
    inc hl
    add hl, bc
    ld a, [$c827]
    ld b, a
    ld a, [$c828]
    ld c, a
    add hl, hl
    add hl, hl
    add hl, bc
    ld bc, $000a
    add hl, bc
    ld a, h
    ld [$c827], a
    ld a, l
    ld [$c828], a
    ld a, [$c823]
    dec a
    ld [$c823], a
    jp Jump_000_395b


Call_000_39dd:
    ld a, [$c820]
    ld b, a
    ld a, [$c822]
    ld c, a
    ld a, [$c821]
    ld d, a
    ld a, [$c823]
    ld e, a
    push bc
    push de
    ld a, b
    sub e
    ld h, a
    ld a, b
    add e
    ld b, a
    ld a, c
    add d
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    ld a, d
    or a
    ret z

    push bc
    push de
    ld a, b
    sub e
    ld h, a
    ld a, b
    add e
    ld b, a
    ld a, c
    sub d
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    ret


Call_000_3a15:
    ld a, [$c820]
    ld b, a
    ld a, [$c822]
    ld c, a
    ld a, [$c821]
    ld d, a
    ld a, [$c823]
    ld e, a
    push bc
    push de
    ld a, b
    sub e
    ld h, a
    ld a, b
    add e
    ld b, a
    ld a, c
    add d
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    push bc
    push de
    ld a, b
    sub e
    ld h, a
    ld a, b
    add e
    ld b, a
    ld a, c
    sub d
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    ld a, d
    sub e
    ret z

    push bc
    push de
    ld a, b
    sub d
    ld h, a
    ld a, b
    add d
    ld b, a
    ld a, c
    sub e
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    push bc
    push de
    ld a, b
    sub d
    ld h, a
    ld a, b
    add d
    ld b, a
    ld a, c
    add e
    ld c, a
    ld d, h
    ld e, c
    call Call_000_3bc5
    pop de
    pop bc
    ret


Call_000_3a71:
    ld a, [$c820]
    ld b, a
    ld a, [$c822]
    ld c, a
    ld a, [$c821]
    ld d, a
    ld a, [$c823]
    ld e, a
    push bc
    push de
    ld a, b
    add d
    ld b, a
    ld a, c
    sub e
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    sub e
    ld b, a
    ld a, c
    sub d
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    sub d
    ld b, a
    ld a, c
    add e
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    add e
    ld b, a
    ld a, c
    add d
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    ld a, d
    or a
    ret z

    sub e
    ret z

    push bc
    push de
    ld a, b
    sub d
    ld b, a
    ld a, c
    sub e
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    sub e
    ld b, a
    ld a, c
    add d
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    add d
    ld b, a
    ld a, c
    add e
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    push bc
    push de
    ld a, b
    add e
    ld b, a
    ld a, c
    sub d
    ld c, a
    call Call_000_3e56
    pop de
    pop bc
    ret


    ld a, [$c820]
    ld b, a
    ld a, [$c821]
    ld c, a
    sub b
    jr nc, jr_000_3b02

    ld a, c
    ld [$c820], a
    ld a, b
    ld [$c821], a

jr_000_3b02:
    ld a, [$c822]
    ld b, a
    ld a, [$c823]
    ld c, a
    sub b
    jr nc, jr_000_3b15

    ld a, c
    ld [$c822], a
    ld a, b
    ld [$c823], a

jr_000_3b15:
    ld a, [$c820]
    ld b, a
    ld d, a
    ld a, [$c822]
    ld c, a
    ld a, [$c823]
    ld e, a
    call Call_000_3bc5
    ld a, [$c821]
    ld b, a
    ld d, a
    ld a, [$c822]
    ld c, a
    ld a, [$c823]
    ld e, a
    call Call_000_3bc5
    ld a, [$c820]
    inc a
    ld [$c820], a
    ld a, [$c821]
    dec a
    ld [$c821], a
    ld a, [$c820]
    ld b, a
    ld a, [$c821]
    ld d, a
    ld a, [$c822]
    ld c, a
    ld e, a
    call Call_000_3bc5
    ld a, [$c820]
    ld b, a
    ld a, [$c821]
    ld d, a
    ld a, [$c823]
    ld c, a
    ld e, a
    call Call_000_3bc5
    ld a, [$c81f]
    or a
    ret z

    ld a, [$c820]
    ld b, a
    ld a, [$c821]
    sub b
    ret c

    ld a, [$c822]
    inc a
    ld [$c822], a
    ld a, [$c823]
    dec a
    ld [$c823], a
    ld a, [$c822]
    ld b, a
    ld a, [$c823]
    sub b
    ret c

    ld a, [$c81c]
    ld c, a
    ld a, [$c81d]
    ld [$c81c], a
    ld a, c
    ld [$c81d], a

jr_000_3b96:
    ld a, [$c820]
    ld b, a
    ld a, [$c821]
    ld d, a
    ld a, [$c822]
    ld c, a
    ld e, a
    call Call_000_3bc5
    ld a, [$c823]
    ld b, a
    ld a, [$c822]
    cp b
    jr z, jr_000_3bb6

    inc a
    ld [$c822], a
    jr jr_000_3b96

jr_000_3bb6:
    ld a, [$c81c]
    ld c, a
    ld a, [$c81d]
    ld [$c81c], a
    ld a, c
    ld [$c81d], a
    ret


Call_000_3bc5:
    ld a, c
    sub e
    jr nc, jr_000_3bcb

    cpl
    inc a

jr_000_3bcb:
    ld [$c825], a
    ld h, a
    ld a, b
    sub d
    jr nc, jr_000_3bd5

    cpl
    inc a

jr_000_3bd5:
    ld [$c824], a
    sub h
    jp c, Jump_000_3d42

    ld a, b
    sub d
    jp nc, Jump_000_3bed

    ld a, c
    sub e
    jr z, jr_000_3bf9

    ld a, $00
    jr nc, jr_000_3bf9

    ld a, $ff
    jr jr_000_3bf9

Jump_000_3bed:
    ld a, e
    sub c
    jr z, jr_000_3bf7

    ld a, $00
    jr nc, jr_000_3bf7

    ld a, $ff

jr_000_3bf7:
    ld b, d
    ld c, e

jr_000_3bf9:
    ld [$c826], a
    ld hl, $5ca7
    ld d, $00
    ld e, c
    add hl, de
    add hl, de
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    ld a, b
    and $f8
    ld e, a
    add hl, de
    add hl, de
    ld a, [$c825]
    or a
    jp z, Jump_000_3ce6

    push hl
    ld h, $00
    ld l, a
    add hl, hl
    ld a, h
    ld [$c829], a
    ld a, l
    ld [$c82a], a
    ld d, h
    ld e, l
    ld a, [$c824]
    cpl
    ld l, a
    ld h, $ff
    inc hl
    add hl, de
    ld a, h
    ld [$c827], a
    ld a, l
    ld [$c828], a
    ld a, [$c824]
    cpl
    ld l, a
    ld h, $ff
    inc hl
    ld a, [$c825]
    ld d, $00
    ld e, a
    add hl, de
    add hl, hl
    ld a, h
    ld [$c82b], a
    ld a, l
    ld [$c82c], a
    pop hl
    ld a, [$c824]
    ld e, a
    ld a, b
    and $07
    add $10
    ld c, a
    ld b, $00
    ld a, [bc]
    ld b, a
    ld c, a

Jump_000_3c5c:
    rrc c
    ld a, [$c827]
    bit 7, a
    jr z, jr_000_3c8d

    push de
    bit 7, c
    jr z, jr_000_3c74

    ld a, b
    cpl
    ld c, a
    call Call_000_3e73
    dec hl
    ld c, $80
    ld b, c

jr_000_3c74:
    ld a, [$c828]
    ld d, a
    ld a, [$c82a]
    add d
    ld [$c828], a
    ld a, [$c827]
    ld d, a
    ld a, [$c829]
    adc d
    ld [$c827], a
    pop de
    jr jr_000_3cce

jr_000_3c8d:
    push de
    push bc
    ld a, b
    cpl
    ld c, a
    call Call_000_3e73
    ld a, [$c826]
    or a
    jr z, jr_000_3ca7

    inc hl
    ld a, l
    and $0f
    jr nz, jr_000_3cb5

    ld de, $0130
    add hl, de
    jr jr_000_3cb5

jr_000_3ca7:
    dec hl
    dec hl
    dec hl
    ld a, l
    and $0f
    xor $0e
    jr nz, jr_000_3cb5

    ld de, $fed0
    add hl, de

jr_000_3cb5:
    ld a, [$c828]
    ld d, a
    ld a, [$c82c]
    add d
    ld [$c828], a
    ld a, [$c827]
    ld d, a
    ld a, [$c82b]
    adc d
    ld [$c827], a
    pop bc
    ld b, c
    pop de

jr_000_3cce:
    bit 7, c
    jr z, jr_000_3cd9

    push de
    ld de, $0010
    add hl, de
    pop de
    ld b, c

jr_000_3cd9:
    ld a, b
    or c
    ld b, a
    dec e
    jp nz, Jump_000_3c5c

    ld a, b
    cpl
    ld c, a
    jp Jump_000_3e73


Jump_000_3ce6:
    ld a, [$c824]
    ld e, a
    inc e
    ld a, b
    and $07
    jr z, jr_000_3d04

    push hl
    add $10
    ld l, a
    ld h, $00
    ld c, [hl]
    pop hl
    xor a

jr_000_3cf9:
    rrca
    or c
    dec e
    jr z, jr_000_3d0c

    bit 0, a
    jr z, jr_000_3cf9

    jr jr_000_3d0c

jr_000_3d04:
    ld a, e
    dec a
    and $f8
    jr z, jr_000_3d33

    jr jr_000_3d18

jr_000_3d0c:
    ld b, a
    cpl
    ld c, a
    push de
    call Call_000_3e73
    ld de, $000f
    add hl, de
    pop de

jr_000_3d18:
    ld a, e
    or a
    ret z

    and $f8
    jr z, jr_000_3d33

    xor a
    ld c, a
    cpl
    ld b, a
    push de
    call Call_000_3e73
    ld de, $000f
    add hl, de
    pop de
    ld a, e
    sub $08
    ret z

    ld e, a
    jr jr_000_3d18

jr_000_3d33:
    ld a, $80

jr_000_3d35:
    dec e
    jr z, jr_000_3d3c

    sra a
    jr jr_000_3d35

jr_000_3d3c:
    ld b, a
    cpl
    ld c, a
    jp Jump_000_3e73


Jump_000_3d42:
    ld a, c
    sub e
    jp nc, Jump_000_3d53

    ld a, b
    sub d
    jr z, jr_000_3d5f

    ld a, $00
    jr nc, jr_000_3d5f

    ld a, $ff
    jr jr_000_3d5f

Jump_000_3d53:
    ld a, c
    sub e
    jr z, jr_000_3d5d

    ld a, $00
    jr nc, jr_000_3d5d

    ld a, $ff

jr_000_3d5d:
    ld b, d
    ld c, e

jr_000_3d5f:
    ld [$c826], a
    ld hl, $5ca7
    ld d, $00
    ld e, c
    add hl, de
    add hl, de
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    ld a, b
    and $f8
    ld e, a
    add hl, de
    add hl, de
    ld a, [$c825]
    ld e, a
    inc e
    ld a, [$c824]
    or a
    jp z, Jump_000_3e35

    push hl
    ld h, $00
    ld l, a
    add hl, hl
    ld a, h
    ld [$c829], a
    ld a, l
    ld [$c82a], a
    ld d, h
    ld e, l
    ld a, [$c825]
    cpl
    ld l, a
    ld h, $ff
    inc hl
    add hl, de
    ld a, h
    ld [$c827], a
    ld a, l
    ld [$c828], a
    ld a, [$c825]
    cpl
    ld l, a
    ld h, $ff
    inc hl
    ld a, [$c824]
    ld d, $00
    ld e, a
    add hl, de
    add hl, hl
    ld a, h
    ld [$c82b], a
    ld a, l
    ld [$c82c], a
    pop hl
    ld a, [$c825]
    ld e, a
    ld a, b
    and $07
    add $10
    ld c, a
    ld b, $00
    ld a, [bc]
    ld b, a
    ld c, a

jr_000_3dc7:
    push de
    push bc
    ld a, b
    cpl
    ld c, a
    call Call_000_3e73
    inc hl
    ld a, l
    and $0f
    jr nz, jr_000_3dd9

    ld de, $0130
    add hl, de

jr_000_3dd9:
    pop bc
    ld a, [$c827]
    bit 7, a
    jr z, jr_000_3df9

    ld a, [$c828]
    ld d, a
    ld a, [$c82a]
    add d
    ld [$c828], a
    ld a, [$c827]
    ld d, a
    ld a, [$c829]
    adc d
    ld [$c827], a
    jr jr_000_3e2b

jr_000_3df9:
    ld a, [$c826]
    or a
    jr nz, jr_000_3e0b

    rlc b
    bit 0, b
    jr z, jr_000_3e15

    ld de, $fff0
    add hl, de
    jr jr_000_3e15

jr_000_3e0b:
    rrc b
    bit 7, b
    jr z, jr_000_3e15

    ld de, $0010
    add hl, de

jr_000_3e15:
    ld a, [$c828]
    ld d, a
    ld a, [$c82c]
    add d
    ld [$c828], a
    ld a, [$c827]
    ld d, a
    ld a, [$c82b]
    adc d
    ld [$c827], a

jr_000_3e2b:
    pop de
    dec e
    jr nz, jr_000_3dc7

    ld a, b
    cpl
    ld c, a
    jp Jump_000_3e73


Jump_000_3e35:
    ld a, b
    and $07
    push hl
    add $10
    ld l, a
    ld h, $00
    ld a, [hl]
    pop hl
    ld b, a
    cpl
    ld c, a

jr_000_3e43:
    push de
    call Call_000_3e73
    inc hl
    ld a, l
    and $0f
    jr nz, jr_000_3e51

    ld de, $0130
    add hl, de

jr_000_3e51:
    pop de
    dec e
    ret z

    jr jr_000_3e43

Call_000_3e56:
    ld hl, $5ca7
    ld d, $00
    ld e, c
    add hl, de
    add hl, de
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    ld a, b
    and $f8
    ld e, a
    add hl, de
    add hl, de
    ld a, b
    and $07
    add $10
    ld c, a
    ld b, $00
    ld a, [bc]
    ld b, a
    cpl
    ld c, a

Call_000_3e73:
Jump_000_3e73:
    ld a, [$c81c]
    ld d, a
    ld a, [$c81e]
    cp $01
    jr z, jr_000_3ea7

    cp $02
    jr z, jr_000_3ec1

    cp $03
    jr z, jr_000_3edb

    ld e, b
    bit 0, d
    jr nz, jr_000_3e8e

    push bc
    ld b, $00

jr_000_3e8e:
    bit 1, d
    jr nz, jr_000_3e94

    ld e, $00

jr_000_3e94:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3e94

    ld a, [hl]
    and c
    or b
    ld [hl+], a
    ld a, [hl]
    and c
    or e
    ld [hl], a
    ld a, b
    or a
    ret nz

    pop bc
    ret


jr_000_3ea7:
    ld c, b
    bit 0, d
    jr nz, jr_000_3eae

    ld b, $00

jr_000_3eae:
    bit 1, d
    jr nz, jr_000_3eb4

    ld c, $00

jr_000_3eb4:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3eb4

    ld a, [hl]
    or b
    ld [hl+], a
    ld a, [hl]
    or c
    ld [hl], a
    ret


jr_000_3ec1:
    ld c, b
    bit 0, d
    jr nz, jr_000_3ec8

    ld b, $00

jr_000_3ec8:
    bit 1, d
    jr nz, jr_000_3ece

    ld c, $00

jr_000_3ece:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3ece

    ld a, [hl]
    xor b
    ld [hl+], a
    ld a, [hl]
    xor c
    ld [hl], a
    ret


jr_000_3edb:
    ld b, c
    bit 0, d
    jr z, jr_000_3ee2

    ld b, $ff

jr_000_3ee2:
    bit 1, d
    jr z, jr_000_3ee8

    ld c, $ff

jr_000_3ee8:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3ee8

    ld a, [hl]
    and b
    ld [hl+], a
    ld a, [hl]
    and c
    ld [hl], a
    ret


Call_000_3ef5:
    ld hl, $5ca7
    ld d, $00
    ld e, c
    add hl, de
    add hl, de
    ld a, [hl+]
    ld h, [hl]
    ld l, a
    ld a, b
    and $f8
    ld e, a
    add hl, de
    add hl, de
    ld a, b
    and $07
    add $10
    ld c, a
    ld b, $00
    ld a, [bc]
    ld c, a

jr_000_3f10:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3f10

    ld a, [hl+]
    ld d, a
    ld a, [hl+]
    ld e, a
    ld b, $00
    ld a, d
    and c
    jr z, jr_000_3f22

    set 0, b

jr_000_3f22:
    ld a, e
    and c
    jr z, jr_000_3f28

    set 1, b

jr_000_3f28:
    ld e, b
    ret


Call_000_3f2a:
    ld hl, $5ca7
    ld d, $00
    ld a, [$c82e]
    rlca
    rlca
    rlca
    ld e, a
    add hl, de
    add hl, de
    ld b, [hl]
    inc hl
    ld h, [hl]
    ld l, b
    ld a, [$c82d]
    rlca
    rlca
    rlca
    ld e, a
    add hl, de
    add hl, de
    ld a, c
    ld b, h
    ld c, l
    ld h, d
    ld l, a
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $53be
    add hl, de
    ld d, h
    ld e, l
    ld h, b
    ld l, c
    ld a, [$c81c]
    ld c, a

jr_000_3f59:
    ld a, [de]
    inc de
    push de
    push hl
    ld hl, $c81d
    ld l, [hl]
    ld b, a
    xor a
    bit 0, l
    jr z, jr_000_3f68

    cpl

jr_000_3f68:
    or b
    bit 0, c
    jr nz, jr_000_3f6e

    xor b

jr_000_3f6e:
    ld d, a
    xor a
    bit 1, l
    jr z, jr_000_3f75

    cpl

jr_000_3f75:
    or b
    bit 1, c
    jr nz, jr_000_3f7b

    xor b

jr_000_3f7b:
    ld e, a
    pop hl

jr_000_3f7d:
    ldh a, [rSTAT]
    bit 1, a
    jr nz, jr_000_3f7d

    ld a, d
    ld [hl+], a
    ld a, e
    ld [hl+], a
    pop de
    ld a, l
    and $0f
    jr nz, jr_000_3f59

    ret


    ld hl, sp+$02
    ld a, [hl+]
    ld [$c82d], a
    ld a, [hl+]
    ld [$c82e], a
    ret


    push bc
    ld a, [$c7a9]
    cp $01
    call nz, $5bbe
    ld hl, sp+$04
    ld a, [hl]
    ld c, a
    call Call_000_3f2a
    call Call_000_391d
    pop bc
    ret


    push bc
    ld hl, sp+$04
    ld a, [hl+]
    ld b, a
    ld a, [hl+]
    ld c, a
    call Call_000_3ef5
    pop bc
    ret


    ld hl, sp+$02
    ld a, [hl+]
    ld [$c81c], a
    ld a, [hl+]
    ld [$c81d], a
    ld a, [hl]
    ld [$c81e], a
    ret


    push bc
    ld a, [$c7a9]
    cp $01
    call nz, $5bbe
    ld hl, sp+$04
    ld a, [hl+]
    ld b, a
    ld a, [hl+]
    ld c, a
    ld a, [hl+]
    ld d, a
    ld a, [hl]
    ld [$c81f], a
    call Call_000_393a
    pop bc
    ret


    push bc
    ld a, [$c7a9]
    cp $01
    call nz, $5bbe
    ld hl, sp+$04
    ld a, [hl+]
    ld [$c820], a
    ld a, [hl+]
    ld [$c822], a
    ld a, [hl+]
    ld [$c821], a
    ld a, [hl+]
    ld [$c823], a
    ld a, [hl]
    db $ea
