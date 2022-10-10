#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#ifdef bool
#undef bool
#endif
typedef short bool;
#define SIZE 100000
bool check_dream(char *key, char *temp)
{
    return strstr(temp,key);
}
const static char *my_dream = "Wanna.w^n";
int main() 
{
    char *buf = malloc(SIZE);
    printf("welcome to Wanna.w^n, this is your gift: %p\n",buf);
    printf("Do you want to know what my dream is?\n");
    printf("You have to find it by yourself ");
    fflush(stdout);
    fgets(buf,SIZE,stdin);
    if(check_dream(my_dream,buf))
    {
        printf("too bad, I wish you could see my dream\n");
        printf("now GET OUT!!!\n");
        exit(-1);
    }
    if(strstr(buf,my_dream))
    {
        printf("yay, congratulation on finding my dream\n");
        printf("I hope you enjoy it <3\n");
        system("/bin/sh");
    }else{
        puts("Goodbye!");
    }

    free(buf);
return 0;
}