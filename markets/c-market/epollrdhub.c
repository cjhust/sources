
/*
 * tcpclient.c - A simple TCP client
 * usage: tcpclient <host> <port>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>


#define BUFSIZE 102400


int main(int argc, char **argv)
{
    int                 rc, n, s, fd, port, size;
    char               *host, *buf, message[BUFSIZE];
    struct sockaddr_in  serveraddr;

    if (argc != 3) {
        fprintf(stderr,"usage: %s <host> <port>\n", argv[0]);
        return -1;
    }
    host = argv[1];
    port = atoi(argv[2]);

    /* socket() */
    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        fprintf(stderr, "socket() faild, %s\n", strerror(errno));
        return -2;
    }

    bzero((char *) &serveraddr, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(port);
    if (inet_pton(AF_INET, host, &serveraddr.sin_addr) != 1) {
        fprintf(stderr, "socket inet_pton() failed, %s\n", strerror(errno));
        return -3;
    }

    /* non-block mode */
    fcntl(s, F_SETFL, fcntl(s, F_GETFL) | O_NONBLOCK);

#if 0
    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 0;
    setsockopt(s, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger));
#endif

    while (1) {
        rc = connect(s, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
        if (rc < 0) {
            fprintf(stderr, "connect() failed, %s\n", strerror(errno));
            sleep(0.1);
        } else {
            break;
        }
    }

    /* send data */
    buf = "POST / HTTP/1.1\r\nHost: www.cjhust.com\r\nContent-Length: 512000305\r\n\r\n";

    n = write(s, buf, strlen(buf));
    if (n < 0) {
        fprintf(stderr, "write() failed, %s", strerror(errno));
        return -4;
    }

    fd = open("/root/cjhust/html/test.mp4", O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "read() failed, %s", strerror(errno));
        return -5;
    }

    size = 0;
    while (1) {
        n = read(fd, message, BUFSIZE);
        n = write(s, message, BUFSIZE);
        if (n < 0) {
            continue;
        }
        size += n;

        if (size >= 16384*20) {
            printf("size = %d\n", size);
            close(s);
            return -6;
        }
    }

    return 0;
}