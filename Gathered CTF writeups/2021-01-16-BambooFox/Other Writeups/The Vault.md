## The Vault
> **Category:** Reverse
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/reverse-the-vault
> **Flag:**
---

`func8` is the password checking code

Mappings from wasm to index.js:
* `import1` -> `fail`
* `import2` -> `win`
* `import3` -> `get_password`

Reverse `func8` to get flag

```
 (func $func7 (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32) (local $var3 i32)
    local.get $var0
    local.set $var1
    block $label2
      block $label0
        local.get $var0
        i32.const 3
        i32.and
        i32.eqz
        br_if $label0
        local.get $var0
        i32.load8_u
        i32.eqz
        if
          i32.const 0
          return
        end
        loop $label1
          local.get $var1
          i32.const 1
          i32.add
          local.tee $var1
          i32.const 3
          i32.and
          i32.eqz
          br_if $label0
          local.get $var1
          i32.load8_u
          br_if $label1
        end $label1
        br $label2
      end $label0
      loop $label3
        local.get $var1
        local.tee $var2
        i32.const 4
        i32.add
        local.set $var1
        local.get $var2
        i32.load
        local.tee $var3
        i32.const -1
        i32.xor
        local.get $var3
        i32.const 16843009
        i32.sub
        i32.and
        i32.const -2139062144
        i32.and
        i32.eqz
        br_if $label3
      end $label3
      local.get $var3
      i32.const 255
      i32.and
      i32.eqz
      if
        local.get $var2
        local.get $var0
        i32.sub
        return
      end
      loop $label4
        local.get $var2
        i32.load8_u offset=1
        local.set $var3
        local.get $var2
        i32.const 1
        i32.add
        local.tee $var1
        local.set $var2
        local.get $var3
        br_if $label4
      end $label4
    end $label2
    local.get $var1
    local.get $var0
    i32.sub
  )
  (func $func8
    (local $var0 i32) (local $var1 i32) (local $var2 i32) (local $var3 i32) (local $var4 i32)
    global.get $global0
    i32.const 32
    i32.sub
    local.tee $var0
    global.set $global0
    call $import3
    local.set $var1
    local.get $var0
    i32.const 1720
    i32.load16_u
    i32.store16 offset=24
    local.get $var0
    i32.const 1712
    i64.load
    i64.store offset=16
    local.get $var0
    i32.const 1704
    i64.load
    i64.store offset=8
    local.get $var0
    i32.const 1696
    i64.load
    i64.store
    block $label2
      block $label0
        local.get $var1
        call $func7
        i32.const 4
        i32.ne
        br_if $label0
        local.get $var1
        i32.load8_u
        i32.const 112
        i32.ne
        br_if $label0
        local.get $var1
        i32.load8_u offset=1
        i32.const 51
        i32.ne
        br_if $label0
        local.get $var1
        i32.load8_u offset=2
        i32.const 107
        i32.ne
        br_if $label0
        local.get $var1
        i32.load8_u offset=3
        i32.const 48
        i32.ne
        br_if $label0
        i32.const 22
        local.set $var3
        local.get $var0
        local.set $var4
        loop $label1
          local.get $var4
          local.get $var1
          local.get $var2
          i32.const 3
          i32.and
          i32.add
          i32.load8_u
          local.get $var3
          i32.xor
          i32.store8
          local.get $var0
          local.get $var2
          i32.const 1
          i32.add
          local.tee $var2
          i32.add
          local.tee $var4
          i32.load8_u
          local.tee $var3
          br_if $label1
        end $label1
        local.get $var0
        call $import2
        br $label2
      end $label0
      call $import1
    end $label2
    local.get $var0
    i32.const 32
    i32.add
    global.set $global0
  )
 ```
 
 
turns out the 
        i32.const 112
        i32.const 51
        i32.const 107
        i32.const 48
was the password
then just override and invoke func to get flag


## References


## Bugs


## Exploit Ideas


## Scripts

