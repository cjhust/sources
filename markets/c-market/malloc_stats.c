#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>


int func1(void)
{
    char *p;

    p = (char *)malloc(1024);
    if (!p)  {
        printf("Malloc error\n");
    }
    return 0;
}


int main()
{
    char *p;

    printf("********Step 1: init **********\n");
    malloc_stats();
    /*
     * system bytes     =     0
     * in use bytes     =     0
     */

    p = (char *)malloc(100);
    if (!p){
        printf("In main ,malloc fail\n");
        return -1;
    }

    printf("\n********Step 2: malloc 100 **********\n");
    malloc_stats();
    /*
     * system bytes     =     135168=132K
     * in use bytes     =        112
     */

    free(p);
    printf("\n********Step 3: free 100 **********\n");
    malloc_stats();
    /*
     * system bytes     =     135168
     * in use bytes     =        0
     */

    func1();
    printf("\n********Step 4: malloc 1024 **********\n");
    malloc_stats();
    /*
     * system bytes     =     135168
     * in use bytes     =       1040
     */

    return 0;
}


