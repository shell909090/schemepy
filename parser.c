#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>

#include "objects.h"

char * control_code = " ()\'\";\r\n";
char * blank_chars = " \t\r\n";
char * find_control_code(char * buf)
{
    while(*buf){
        if(strchr(control_code, *buf) != NULL) return buf;
        ++buf;
    }
    return NULL;
}

char * find_quota_end(char * buf)
{
    while(*buf){
        if(*buf == '"' && *(buf-1) != '\\') return buf + 1;
        ++buf;
    }
    return NULL;
}

typedef int (*FPT_PROC_CHUNK)(void * handler, char * chunk, int size);
int proc_buf(FPT_PROC_CHUNK callback, void * handler, char * buf)
{
    int bufsize;
    int result;
    char * start;
    char * chunk_pos;
    
    bufsize = strlen(buf);
    start = buf;
    while(start - buf < bufsize){
        chunk_pos = find_control_code(start);
        if(chunk_pos == NULL) break;
        result = callback(handler, start, chunk_pos - start);
        if(result < 0) return result;
        if(strchr(blank_chars, *chunk_pos) != NULL){
            start = chunk_pos + 1;
            continue;
        }
        switch(*chunk_pos){
        case '"':
            start = find_quota_end(chunk_pos+1);
            if(start == NULL) perror("quota not match");
            else{
                result = callback(handler, chunk_pos, start - chunk_pos);
                if(result < 0) return result;
            }
            break;
        case ';':
            start = strchr(chunk_pos, '\n');
            if(start == NULL) start = buf + bufsize;
            else start += 1;
            break;
        default:
            callback(handler, chunk_pos, 1);
            start = chunk_pos + 1;
            break;
        }
    };
    return 0;
}

int proc_chunk(void * handler, char * chunk, int size)
{
    SString * obj_str;
    char buf[size+1];
    if(size == 0) return 0;
    obj_str = screate_string(chunk, size);
    strncpy(buf, chunk, size);
    buf[size] = 0;
    printf("chunk: %s\n", buf);
    return 0;
}

int main(int argc, char * argv[])
{
    int fileno;
    size_t filesize;
    void * buf;
    if (argc < 2){
        printf("useage: %s filename", argv[0]);
        return 0;
    }
    fileno = open(argv[1], O_RDONLY);
    filesize = lseek(fileno, 0, SEEK_END);
    lseek(fileno, 0, SEEK_SET);
    buf = mmap(NULL, filesize, PROT_READ, MAP_SHARED, fileno, 0);
    close(fileno);
    printf("%s", buf);
    proc_buf(proc_chunk, NULL, buf);
    munmap(buf, filesize);
    return 0;
}
