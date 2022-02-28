package main

import (
  "bytes"
  "crypto/md5"
  "encoding/binary"
  "encoding/hex"
  "fmt"
  "gopkg.in/alecthomas/kingpin.v2"
  "io/ioutil"
  "log"
  "math/bits"
  "os"
)

var (
  enc = kingpin.Flag("encrypt", "Encrypt").Bool()
  dec = kingpin.Flag("decrypt", "Decrypt").Bool()
  keyFile = kingpin.Flag("key", "Key").Required().ExistingFile()
)

func main() {
  kingpin.HelpFlag.Short('h')
  kingpin.Parse()
  if *enc == *dec {
    log.Fatal("error: Exactly one of --encrypt and --decrypt is required.")
  }

  key, err := ioutil.ReadFile(*keyFile)
  if err != nil {
    log.Fatal(err)
  }
  if len(key) != 24 {
    log.Fatal("keys should be exactly 24 bytes.")
  }

  content, err := ioutil.ReadAll(os.Stdin)
  if err != nil {
    log.Fatal(err)
  }

  if *enc {
    ciphertext := encrypt(content, key)
    fmt.Print(ciphertext)
  } else if *dec {
    plaintext := decrypt(string(content), key)
    os.Stdout.Write(plaintext)
  }
}

func encrypt(plaintext []byte, key []byte) string {
  x := uint64(binary.LittleEndian.Uint64(key[0:]))
  y := uint64(binary.LittleEndian.Uint64(key[8:]))
  z := uint64(binary.LittleEndian.Uint64(key[16:]))

  keyid := md5.Sum(key)
  r := keyid[:]
  for _, e := range plaintext {
    t := (e - byte(x)) ^ byte(y) ^ byte(z)
    r = append(r, t)
    x = bits.RotateLeft64(x, -1)
    y = bits.RotateLeft64(y, 1)
    z = bits.RotateLeft64(z, 1)
  }
  return hex.EncodeToString(r)
}

func decrypt(ciphertext string, key []byte) []byte {
  ciphertext_bytes, err := hex.DecodeString(string(ciphertext))
  if err != nil {
    log.Panic(err)
  }

  keyid := md5.Sum(key)
  r := keyid[:]
  if (!bytes.Equal(r, ciphertext_bytes[0:len(r)])) {
    //log.Panic("invalid key")
  }
  ciphertext_bytes = ciphertext_bytes[len(keyid):]

  x := uint64(binary.LittleEndian.Uint64(key[0:]))
  y := uint64(binary.LittleEndian.Uint64(key[8:]))
  z := uint64(binary.LittleEndian.Uint64(key[16:]))

  r = make([]byte, 0, len(ciphertext_bytes))
  for _, e := range ciphertext_bytes {
    t := (e ^ byte(y) ^ byte(z)) + byte(x)
    r = append(r, t)
    x = bits.RotateLeft64(x, -1)
    y = bits.RotateLeft64(y, 1)
    z = bits.RotateLeft64(z, 1)
  }
  return r
}
