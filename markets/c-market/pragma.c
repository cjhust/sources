#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* sizeof() = 24 */
struct test1 {
    char   x1;
    char   x2;
    double x3;
    char   x4;
};


/* sizeof() = 16 */
struct test2 {
    double x3;
    char   x1;
    char   x2;
    char   x4;
};


/* sizeof() = 11 */
#pragma pack(1)
struct test3 {
    char   x1;
    char   x2;
    double x3;
    char   x4;
};
#pragma pack()


/* sizeof() = 12 */
#pragma pack(2)
struct test4 {
    char   x1;
    char   x2;
    double x3;
    char   x4;
};
#pragma pack()


int main()
{
    printf("sizeof(test1) = %lu\n", sizeof(struct test1));
    printf("sizeof(test2) = %lu\n", sizeof(struct test2));
    printf("sizeof(test3) = %lu\n", sizeof(struct test3));
    printf("sizeof(test4) = %lu\n", sizeof(struct test4));

    return 0;
}

