//Pretend there's already a text file with an order waiting.

#include <stdio.h>

int main(){
    FILE *ptrFile;
    char buf[1000]
    
    ptrFile = fopen("test.txt", "r")
    if (!ptrFile) {
        return 1;
    }
    while (fgets(buff, 1000, ptrFile) != NULL) {
        printf("%s", buf);
    }
    
    fclose(ptrFile);
    return 0;
}

