# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

lung disease caused by inhaling very fine ash and sand dust; longest word in most English dictionaries

## According to its man page, what does `getrusage` do?

get resource usage; takes in an int, and a struct rusage and returns resources usage measue for things
like usage statistics for the calling process, for calling thread, etc.
stats include user CPU time, system CPU time, integral shared memory size, etc.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16; but not all variable fields are completes or used and are thus by default set to zero

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

the code is as follows in speller:

    getrusage(RUSAGE_SELF, &before);
    bool loaded = load(dictionary);
    getrusage(RUSAGE_SELF, &after);

An if statement later, we see time_load = calculate(&before, &after).
Although it seems we might not be changing the contents, just like what we have seen with the gatorade
swap example, we use & and * to change the values of variables `before` and `after` which are garbage
values prior to applying getursage(). Without the pointers, the function will perform correctly but
will not return/change the values of variables `before` and `after`.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

1.) the for loop takes in one character (variable c) of a text file at a time
2.) variable 'c' is added into an array 'word' if it is part of the alphabet or is an apostrophe (ignores numbers)
3.) continues to add next values for c into array 'word' until we reach EOF, we leave the scanning loop
4.) if the word is too long (too long to be an actual word) or is a number, we clear the index, and prepare for a new word
4.) if the index is not empty (meaning there is a word we have completed), we cap it with "\0" null character
5.) update word counter
6.) check word (array 'word') for spelling, return true or false
7.) if misspelled (true) then print the misspelled word and add increment misspelled word counter by one
8. next we update our elapsed time
9.) clear index to zero and get ready for next word
10.) return to beginning of for loop to scan in more chars for variable c


## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

reason 1: fscaf takes into account all characters and stops once it reaches a "space" character. Thus,
for a word at the end of a sentence, it will copy in the punctuation.

reason 2: if a a very long string (potentially malicious in intent) was to be be scanned by `fscanf`,
memory of important information could be overwritten or cause segmentation fault.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

The parameter for check is variable "word". The parameter for load is variable "dictionary". Since we
do not want to mutate or change our scanned-in word or dictionary in any way, we should declare them as
`const`.
