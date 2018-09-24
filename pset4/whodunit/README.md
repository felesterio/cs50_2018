# Questions

## What's `stdint.h`?

<stdint.h> is a header that delcares sets of integer types with specified widths,
and also defines sets of macros that specify limits of integer types defined in other headers.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

It is a specific data type. Just like integers, you place these before defining a variable.
However, these specify further charactersitics of an integer. 8 bits, `uint32_t` is an
unsigned long long, `int32_t` is a signed long long, and a `uint16_t` is an unsigned 16 bit int.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE`: 1, `DWORD`: 4, `LONG`: 4, `WORD`: 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

ascii "BM", hex 0x4D42

## What's the difference between `bfSize` and `biSize`?

bfSize is the total number of bytes in the file. biSize is the number of bytes in the info header.

## What does it mean if `biHeight` is negative?

If biHeight == +value, bitmap is a bottom-up DIB (device-independent bitmap) and its origin is the lower left corner.
If biHeight == -value, the bitmap is a top-down DIB (device-independent bitmap) and its origin is the upper left corner.


## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the file to open does not exist, then fopen will return NULL

## Why is the third argument to `fread` always `1` in our code?

The program reads the file one struct (ie byte, WORD, DWORD, LONG) at a time

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3 pixel width means 3*3 = 9 total bytes. BMP's are stored differently if the number of bytes
in a scan line is not a multiple of 4. Therefore we must add 3 (assign 3 to padding) bytes.

## What does `fseek` do?

declares where in the file the program continues/starts scanning the file by inputting a specified offset from the start

## What is `SEEK_CUR`?

value specified by program and used in fseek to set the offset relative to the current pointer position;
as stated by the comment, it is utilized to skip over any padding in the txt file
