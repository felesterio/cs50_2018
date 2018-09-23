#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //initialize variables
    int n;



    //prompt user for a height btw 0 and 23 inclusive
    do
    {
        n = get_int("Height of Pyramid (between 0 and 23)?: ");
    }
    while (n < 0 || n > 23);





    //Print out pyramid
    for (int i = 1; i <= n; i++)
    {
        //for left space
        for (int j = 1; j <= n - i; j++)
        {
            printf(" ");
        }

        //for left pyramid
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }

        //middle space
        printf("  ");

        //for right pyramid
        for (int l = 0; l < i; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}