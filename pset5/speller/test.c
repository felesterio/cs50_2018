// Implements a dictionary's functionality
//this is the LINKED LIST HASTABLE VERSION

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include  <string.h>
#include <ctype.h>
#include "dictionary.h"

//make up our node for a linked list
typedef struct node
{
    char word[LENGTH +1];
    struct node *next;
}
node;

//hash table
node *hashtable[26] = {NULL};

int count = 0;

const char * common_words[] = {
    "the",
    "of",
    "and",
    "to",
    "a",
    "in",
    "is",
    "i",
    "that",
    "it",
    "for",
    "you",
    "was",
    "with",
    "on",
    "as",
    "have",
    "but",
    "be",
    "they",
    "he",
    "she",
};

bool check(const char *word)
{
    char word_cpy[LENGTH +1] = {'\0'};
    strcpy(word_cpy, word);
    //do we need to worry about punctuation????
    int x = 0;
    while (word_cpy[x] != '\0')
    {
        word_cpy[x] = tolower(word_cpy[x]);
        x++;
    }
    printf("%s\n", word_cpy);

    //top commonly used words
    for (int i = 0; i < 22; i++)
    {
        if (strcmp(word_cpy, common_words[i]) == 0)
        {
            return true;
        }
    }

    //if not common, look in loaded dictionary
    int i = word[0]-97;

    if (hashtable[i] != NULL)
    {
        node *cursor = hashtable[i];
        while(cursor != NULL)
        {
            if (strcmp(word_cpy, cursor -> word) == 0)
            {
                return true;
            }

            cursor = cursor -> next;
            }
        free(cursor);
    }

    //if we finish the for loop, then do this
    return false;
}

bool load(const char *dictionary)
{
    //open dictionary

    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return false;
    }

    //get the word
    char word[LENGTH +1];
    while (fscanf(inptr, "%s", word) != EOF)
    {
        //load up node
        node *new_entry = malloc(sizeof(node));
        new_entry -> next = NULL;
        //if we run out of memory
        if (new_entry == NULL)
        {
            free(new_entry);
            return false;
        }
        //else, successful
        strcpy(new_entry -> word, word);
        count++;

        //hashfunction; a is hastable[0], b is hastable[1]
        int hashtable_index = word[0]-97;

        //link nodes in linked list

        //if the linked isnt initialized yet
        if (hashtable[hashtable_index] == NULL)
        {
            hashtable[hashtable_index] = new_entry;
        }

        //if intialized
        else
        {
            new_entry -> next = hashtable[hashtable_index];
            hashtable[hashtable_index] = new_entry;
        }
    }

    //TAKE NOTE:
    //in my linked list, last word goes first ie azuza is first in the list, last on the list is aaa
    //also, hashtable[index] CONTAINS A WORD, meaning:
    //printf("%s\n", hashtable[0] -> word); exists

    return true;
}

bool unload(void)
{
    //free up memory from linked list
    for (int i = 0; i < 26; i++)
    {
        if (hashtable[i] != NULL)
        {
            node *cursor = hashtable[i];
            while(cursor != NULL)
            {
                node *temp = cursor;
                cursor = cursor -> next;
                //printf("%s\n", cursor -> word);
                //^shows every dictionary word
                free(temp);
            }
            free(cursor);
        }
    }

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

int main (void)
{
    load("large");
    printf("%i\n", size());
    printf("%d\n", check("cRayFIsh"));
    unload();
}
