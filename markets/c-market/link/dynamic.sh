gcc -c foo.c -o foo.o -Wall -fPIC
gcc -shared -o libfoo.so foo.o
gcc -c test.c -o test.o
gcc test.o -o test -Wl,-rpath,'.' -L . -lfoo
./test
