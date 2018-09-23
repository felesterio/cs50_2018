#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
int main(int argc, string argv[])

{
    //KEY IS ARGV[1]
    string key =  argv[1];

    // too many too little arguements
    if (argc != 2)
    {
        printf("Usage: %s k\n", argv[0]);
        return 1;
    }

    //check if its all char
    int i = 0;
    int length_key;
    for (length_key = 0; key[length_key] != '\0'; ++length_key);
    while (i < length_key)
    {
        if (isalpha(key[i]))
        {
            key[i] = tolower(key[i]);
            i += 1;
        }
        else
        {
            printf("Usage: %s k\n", argv[0]);
            return 1;
        }
    }

    //certified key is ready to use

    //encipher function
    if (argc == 2)
    {
        //get the plaintext
        string plaintext = get_string("plaintext: ");
        int length_pt;
        for (length_pt = 0; plaintext[length_pt] != '\0'; ++length_pt);
        int index_key = 0;
        int index_plaintext = 0;
        char output[length_pt + 1];

        while (index_plaintext < length_pt)
        {
            char p_x = plaintext[index_plaintext];
            char k_x = key[index_key % (length_key)];

            //if alphabetic
            if (isalpha(p_x))
            {
                //not capital
                if islower(p_x)
                {
                    int pt_ascii = p_x;
                    int shift = k_x - 97;
                    int shifted = (pt_ascii + shift);
                    if (shifted > 122)
                    {
                        int shifted_new = shifted % 122;
                        shifted = 96 + shifted_new;
                    }
                    char new_pt = shifted;
                    output[index_plaintext] = new_pt;
                    index_plaintext += 1;
                    index_key += 1;
                }

                //capital
                if isupper(p_x)
                {
                    int pt_ascii = p_x;
                    int shift = k_x - 97;
                    int shifted = (pt_ascii + shift);
                    if (shifted > 90)
                    {
                        int shifted_new = shifted % 90;
                        shifted = 64 + shifted_new;
                    }
                    char new_pt = shifted;
                    output[index_plaintext] = new_pt;
                    index_plaintext += 1;
                    index_key += 1;
                }
            }

            //not an alphabetic char
            else
            {
                output[index_plaintext] = p_x;
                index_plaintext += 1;
            }

            output[index_plaintext] = '\0';

        }

        printf("ciphertext: %s\n", output);

    }

}