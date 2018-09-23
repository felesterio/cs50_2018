#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{
    double c4 = pow(2, -9.0/12.0)*440;
    printf("%f\n", c4);
}
