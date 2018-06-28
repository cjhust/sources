CC = gcc
CFLAGS = -g -O0 -fPIC -Wall -lpthread
B_OBJ = backtrace epollrdhub malloc_stats sprintf pragma
N_OBJ = client_body_timeout client_header_timeout

all: $(N_OBJ)


client_body_timeout: client_body_timeout.o
	$(CC) $^ $(CFLAGS) -o $@

client_header_timeout: client_header_timeout.o
	$(CC) $^ $(CFLAGS) -o $@

backtrace: backtrace.o
	$(CC) $^ $(CFLAGS) -rdynamic -o $@

epollrdhub: epollrdhub.o
	$(CC) $^ $(CFLAGS) -o $@

malloc_stats: malloc_stats.o
	$(CC) $^ $(CFLAGS) -o $@

sprintf: sprintf.o
	$(CC) $^ $(CFLAGS) -o $@

pragma: pragma.o
	$(CC) $^ $(CFLAGS) -o $@

clean:
	rm -f $(B_OBJ) $(N_OBJ) *.o

