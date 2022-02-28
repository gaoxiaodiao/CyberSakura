package main

import ( 
	"fmt"
	"io/ioutil"
	"os"
	"crypto/md5"
)

func check( e error ) {
    if e != nil {
        panic( e )
    }
}

func gen_key( seed string ) string {
	if len( seed ) < 6 {
		for i := 0; i < 6 - len( seed ); i++ {
			seed += "0"
		}
	} else if len( seed ) > 6 {
		seed = seed[0:6]
	}

	return seed
}

func encrypt ( data []byte, key [16]byte ) {
	for i := 0; i < len( data ); i++ {
		data[ i ] ^= key[ i % len( key ) ]
	}
}

func main() {

	var (
		file string
		seed string
	)

	if len( os.Args ) > 2 {
		file = os.Args[ 1 ]
		seed = os.Args[ 2 ] 
	} else {
		fmt.Println( "Usage go run " + os.Args[ 0 ] + " <file> <seed>" )
		os.Exit( -1 )
	}

	data, err := ioutil.ReadFile( file )
	check( err )

	key := md5.Sum( []byte( gen_key( seed ) ) )
	fmt.Printf("%x", key)

	encrypt( data, key )

	err = ioutil.WriteFile( file + ".enc" , data, 0644 )
    check( err )

}
