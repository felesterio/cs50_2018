#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    char *hash =  argv[1];
    char guess_2[3];
    char guess_3[4];
    char guess_4[5];
    char guess_5[6];
    guess_2[2] = '\0';
    guess_3[3] = '\0';
    guess_4[4] = '\0';
    guess_5[5] = '\0';

    // too many too little arguements
    if (argc != 2)
    {
        printf("Usage: %s hash\n", argv[0]);
        return 1;
    }

    //start crackin
    //to reader: originally i wanted to sift through all ascii values
    //ascii values from 32 to 126 (all characters you can type on a keyboard)
    //id convert ascii int to char, and then from there find the password
    // it took too long, and i decided to take two risks to make up in speed
    // 1.) I assumed that the password is all alphabetic symbols,
    // thus, i gave up on the ASCII conversion and instead made an alphabet string
    // 2.) i did not make code to break a one or two digit password because
    //  i would assume not many (if it all) would make a one digit password
    //if they did, they would've fooled me; at least with less code, crack.c should run
    // a little faster without it

    char salt[2];
    //get salt
    for (int i = 0; i < 2; i++)
    {
        salt[i] = hash[i];
    }

    char *alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";


    //edit: it seems i might need code for TWO LETTER passwords after all...
    for (int i = 0; i < 52; i++)
    {
        char ASCII_i = alphabet[i];

        for (int j = 0; j < 52; j++)
        {
            char ASCII_j = alphabet[j];
            guess_2[0] = ASCII_i;
            guess_2[1] = ASCII_j;
            char *check = crypt(guess_2, salt);
            if (strcmp(check, hash) == 0)
            {
                printf("%s\n", guess_2);
                return 0;
            }
        }
    }

    //check for three characters
    for (int i = 0; i < 52; i++)
    {
        char ASCII_i = alphabet[i];

        for (int j = 0; j < 52; j++)
        {
            char ASCII_j = alphabet[j];

            for (int k = 0; k < 52; k++)
            {
                char ASCII_k = alphabet[k];
                guess_3[0] = ASCII_i;
                guess_3[1] = ASCII_j;
                guess_3[2] = ASCII_k;
                char *check = crypt(guess_3, salt);
                if (strcmp(check, hash) == 0)
                {
                    printf("%s\n", guess_3);
                    return 0;
                }
            }
        }
    }

    //check for four characters
    // it takes an average of one minute to a go through all combos 1,2,3,4 characters long
    for (int i = 0; i < 52; i++)
    {
        char ASCII_i = alphabet[i];

        for (int j = 0; j < 52; j++)
        {
            char ASCII_j = alphabet[j];

            for (int k = 0; k < 52; k++)
            {
                char ASCII_k = alphabet[k];

                for (int l = 0; l < 52; l++)
                {
                    char ASCII_l = alphabet[l];
                    guess_4[0] = ASCII_i;
                    guess_4[1] = ASCII_j;
                    guess_4[2] = ASCII_k;
                    guess_4[3] = ASCII_l;
                    char *check = crypt(guess_4, salt);
                    if (strcmp(check, hash) == 0)
                    {
                        printf("%s\n", guess_4);
                        return 0;
                    }

                }
            }
        }
    }

    //for five characters
    //to find zzzzz, it takes about AN HOUR to reach get to that combo
    for (int i = 0; i < 52; i++)
    {
        char ASCII_i = alphabet[i];

        for (int j = 0; j < 52 ; j++)
        {
            char ASCII_j = alphabet[j];

            for (int k = 0; k < 52; k++)
            {
                char ASCII_k = alphabet[k];

                for (int l = 0; l < 52 ; l++)
                {
                    char ASCII_l = alphabet[l];

                    for (int m = 0; m < 52; m++)
                    {
                        char ASCII_m = alphabet[m];

                        guess_5[0] = ASCII_i;
                        guess_5[1] = ASCII_j;
                        guess_5[2] = ASCII_k;
                        guess_5[3] = ASCII_l;
                        guess_5[4] = ASCII_m;
                        char *check = crypt(guess_5, salt);
                        if (strcmp(check, hash) == 0)
                        {
                            printf("%s\n", guess_5);
                            return 0;
                        }
                    }
                }
            }
        }
    }
}