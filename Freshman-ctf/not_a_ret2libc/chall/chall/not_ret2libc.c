#include <stdio.h>

int main()
{
    char buf;
    write(1,"give me something please: ",0x1b);
    gets(&buf);
return 0;
}