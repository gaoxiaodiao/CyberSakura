## Xorpainter (Misc, 4p)
	
	you need a BIG screen to solve this problem 
	
###ENG
[PL](#pl-version)

317MB CSV file is provided. Each row contains 4 numbers.
It looks like first pair is always smaller than the second pair.
This suggests the numbers represent rectangles.
Name of the file suggests we should paint them in xor mode (like in AWT).

The data is huge, so we do one simple optimization.
Instead of painting all the pixels, we mark only first and last row of each rectangle.

For example, for input:

	0, 0, 3, 3
	2, 2, 4, 4

following image is generated:

	1 1 1 0
	0 0 0 0
	1 1 0 1
	0 0 1 1

after XORing each row with previous one, end result is generated:

	1 1 1 0
	1 1 1 0
	1 1 0 1
	0 0 1 1

After this optimization, processing all the data takes only a couple of minutes.
The result is 16384x16384 image. ImageMagick is able to load and navigate through such big image.
Some letters are visible, but it's mostly empty space.
The image becomes more usefull after removing empty rows and columns.
```cpp
#include <stdio.h>
#include <stdlib.h>

#define size 16384

static int flip[size][size];
static int non_empty_x[size];
static int non_empty_y[size];

int main(int argc, char*argv[]) {
	int x0,y0,x1,y1;
	int row = 0;
	while(scanf("%d, %d, %d, %d", &x0, &x1, &y0, &y1) == 4) {
		for(int x=x0;x<x1;x++){
			flip[y0][x]^=1;
			flip[y1][x]^=1;
		}
		row++;
		if((row&0xfff) == 0) {
			fprintf(stderr, "row: %d\r", row);
		}
	}	

	row = 0;
	for(int y=1;y<size;y++){
		for(int x=0;x<size;x++){
			flip[y][x] ^= flip[y-1][x];
		}
		row++;
		if((row&0xfff) == 0) {
			fprintf(stderr, "flip: %d\r", row);
		}
	}

	for(int y=0;y<size;y++){
		for(int x=0;x<size;x++){
			non_empty_x[x] |= flip[y][x];
			non_empty_y[y] |= flip[y][x];
		}
	}

	int xsize = 0;
	int ysize = 0;

	for(int i=0;i<size;i++){
		xsize += non_empty_x[i];
		ysize += non_empty_y[i];
	}


	printf("P1 %d %d\n",xsize,ysize);
	for(int y=0;y<size;y++){
		for(int x=0;x<size;x++){
			if(non_empty_x[x] && non_empty_y[y]) {
				printf("%d ",flip[y][x]);
			}
		}
		printf("\n");
	}
}
```
It looks like only outlines of the letters are visible - probably due to off by one error.
The image is also still 3195 x 3321 pixels, but we can read a flag from it.

`0ctf{5m@LL_fL@g_#n_BiG_Bitmap}`

###PL version

Otrzymujemy 317 megabajtowy plik CSV.
Ka??dy wiersz zawiera 4 liczby.
Pierwsza para jest zawsze mniejsza ni?? druga para.
Sugeruje to ??e warto??ci reprezentuj?? prostok??ty (x0, y0, x1, y1).
Nazwa pliku sugeruje ??e powinni??my je namalowa?? trybem XOR (jak w AWT).

Dane s?? jednak zbyt du??e dla naiwnego algorytmu.
Stosujemy wi??c prost?? optymalizacj??.
Zamiast malowa?? ka??dy piksel, malujemy tylko pierwszy i ostatni rz??d ka??dego prostok??ta.

Np. dla wej??cia:

	0, 0, 3, 3
	2, 2, 4, 4

generowana jest bitmapa:

	1 1 1 0
	0 0 0 0
	1 1 0 1
	0 0 1 1

po sXORowaniu ze sob?? kolejnych rz??d??w otrzymujemy ostateczny obraz: 

	1 1 1 0
	1 1 1 0
	1 1 0 1
	0 0 1 1

Po tej optymalizacji, przetworzenie danych zajmuje tylko kilka minut.
Wynikiem jest bitmapa 16384x16384 pikseli.
ImageMagick (jako jeden z nielicznych) potrafi otworzy?? i nawigowa?? po tak wielkim obrazie.
Widoczne s?? jakie?? litery, ale wi??kszo???? obrazka jest pusta.
Aby zwi??kszo???? czytelno???? usuwamy puste wiersze i kolumny.
```cpp
#include <stdio.h>
#include <stdlib.h>

#define size 16384

static int flip[size][size];
static int non_empty_x[size];
static int non_empty_y[size];

int main(int argc, char*argv[]) {
	int x0,y0,x1,y1;
	int row = 0;
	while(scanf("%d, %d, %d, %d", &x0, &x1, &y0, &y1) == 4) {
		for(int x=x0;x<x1;x++){
			flip[y0][x]^=1;
			flip[y1][x]^=1;
		}
		row++;
		if((row&0xfff) == 0) {
			fprintf(stderr, "row: %d\r", row);
		}
	}	

	row = 0;
	for(int y=1;y<size;y++){
		for(int x=0;x<size;x++){
			flip[y][x] ^= flip[y-1][x];
		}
		row++;
		if((row&0xfff) == 0) {
			fprintf(stderr, "flip: %d\r", row);
		}
	}

	for(int y=0;y<size;y++){
		for(int x=0;x<size;x++){
			non_empty_x[x] |= flip[y][x];
			non_empty_y[y] |= flip[y][x];
		}
	}

	int xsize = 0;
	int ysize = 0;

	for(int i=0;i<size;i++){
		xsize += non_empty_x[i];
		ysize += non_empty_y[i];
	}


	printf("P1 %d %d\n",xsize,ysize);
	for(int y=0;y<size;y++){
		for(int x=0;x<size;x++){
			if(non_empty_x[x] && non_empty_y[y]) {
				printf("%d ",flip[y][x]);
			}
		}
		printf("\n");
	}
}
```
Tylko kraw??d?? liter jest widoczna - prawdobodobnie powinni??my u??y?? <= zamiast <.
Obrazek nadal ma a?? 3195 x 3321 pikseli.
Nie przeszkadza to jednak w odczytaniu flagi.

`0ctf{5m@LL_fL@g_#n_BiG_Bitmap}`
