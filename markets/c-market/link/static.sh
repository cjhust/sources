gcc -c foo.c -o foo.o -Wall -fPIC
ar -c -r -s libfoo.a foo.o
gcc -c test.c -o test.o
gcc test.o -o test libfoo.a 
./test
