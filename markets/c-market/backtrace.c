
/*
 * gcc -g -rdynamic backtrace.c -o backtrace
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>	    /* for signal */
#include <execinfo.h>	/* for backtrace() */


#define SIZE	100


void dump(void)
{
	int    i, nptrs;
	void  *buffer[SIZE];
	char  **strings;

	nptrs = backtrace(buffer, SIZE);
	printf("backtrace() returned %d addresses: \n", nptrs);

	strings = backtrace_symbols(buffer, nptrs);
	if (strings == NULL) {
		perror("backtrace_symbols");
		exit(EXIT_FAILURE);
	}

	for (i = 0; i < nptrs; i++) {
		printf("[%02d] %s\n", i, strings[i]);
	}

	free(strings);
}


/*
 * 使用static修饰函数，表明不导出这个符号。
 * 即使用-rdynamic选项，看到的只能是个地址。
 */
static void myfunc2()
{
	dump();
}


void myfunc()
{
	myfunc2();
}


int main(int argc, char *argv[])
{
	myfunc();
	return 0;
}
