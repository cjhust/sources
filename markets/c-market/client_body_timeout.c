
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
    int                 rc, n, s, port, size;
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
    buf = "GET / HTTP/1.1\r\nHost: www.cjhust.com\r\nContent-Length: 512\r\n\r\n";

    n = write(s, buf, strlen(buf));
    if (n < 0) {
        fprintf(stderr, "write() failed, %s", strerror(errno));
        return -5;
    }

    sleep(10);
    
    /* recv data */
    size = 0;
    while (1) {
        n = read(s, message, BUFSIZE);
        if (n < 0) {
            if (errno == EAGAIN) {
                sleep(0.1);
                continue;     
            } else {
                fprintf(stderr, "read() failed, %s", strerror(errno));
                return -6;
            }       
        }

        if (n == 0) {
            break;
        }

        size += n;    
    }   
    fprintf(stdout, "size = %d\n", size);     
    close(s);

    return 0;
}