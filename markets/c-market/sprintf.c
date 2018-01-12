#include <stdio.h>


/*
 * result: hello123
 * result: hello
 */
void base()
{
    char buf[10];
    sprintf(buf, "%s:%d", "hello", 123);
    printf("%s\n", buf);

    sprintf(buf, "%s", "hello");
    printf("%s\n", buf);
}


/*
 * result: coredump
 */
void test()
{
    char buf[10];
    sprintf(buf, "The length of the string is more than 10");
    printf("%s", buf);
}


int main()
{
    base();
    test();

    return 0;
}

