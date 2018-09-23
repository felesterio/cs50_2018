// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    //take in fraction "X/Y"
    //assumes num and den are any digit
    //return number of eighth note counts it is

    //find the position of slash in fraction
    int length = strlen(fraction);
    string slash = strchr(fraction, '/');
    int slash_pos = (int)(slash - fraction);

    //using that, you can find substring num_s
    char num_s[slash_pos + 1];
    strncpy(num_s, fraction + 0, slash_pos - 0);

    //likewise, find substring den_s
    char den_s[length - slash_pos];
    strncpy(den_s, fraction + slash_pos + 1, length - slash_pos + 1);

    //convert to ints
    int denominator = atoi(den_s);
    int numerator = atoi(num_s);

    //find number of eight notes
    double eighth_notes = (double)numerator / (double)denominator;
    eighth_notes = 8 * eighth_notes;
    return eighth_notes;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    //note = "(note w/o accidental(#/b)(octave)
    //parse the string into a note and its octave
    int length = strlen(note);
    char letter = note[0];
    int octave = note[length - 1];
    octave -= 48;
    bool accidental;
    if (length == 2)
    {
        accidental = false;
    }
    if (length == 3)
    {
        accidental = true;
    }

    //calculate freq of note in given octave (hz)
    //A4 = 440 Hz
    //for every semitone up multiply 2^(1/12)
    //for every semitone down divide by 2^(1/12)
    //A5 = 2^(12/12)
    // we will be doing it relative to C4 instead, since octaves change relative to octaves of C


    //_ means black keys
    string keyboard = "C_D_EF_G_A_B";


    double c4 = pow(2, (-9.0 / 12.0)) * 440;
    string key_note = strchr(keyboard, letter);
    int semitone = (int)(key_note - keyboard);

    if (octave >= 4)
    {
        semitone = (octave - 4.0) * 12 + semitone;
    }

    if (octave < 4)
    {
        semitone = semitone - 12;
        semitone = (octave - 3.0) * 12 + semitone;
    }

    if (accidental ==  true)
    {
        if (note[1] == '#')
        {
            semitone = semitone + 1;
        }
        if (note[1] == 'b')
        {
            semitone = semitone - 1;
        }
    }

    //return freq
    int frequency = round(c4 * pow(2, semitone / 12.0));

    return frequency;


}


// Determines whether a string represents a rest
bool is_rest(string s)
{
    //if s represents  rest, returns true; otherwise, returns false
    if (strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

