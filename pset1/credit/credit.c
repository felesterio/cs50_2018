#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //intialize variables
    long long ccnum;
    int even_sum = 0;
    int odd_sum = 0;

    //rejects negatives, zero, hyphens
    do
    {
        ccnum = get_long_long("Enter a credit card number: ");
    }
    while (ccnum <= 0);

    //test 1, valid credit card
    int n = 1;
    double index = pow(10, n);
    int nDigits = floor(log10(llabs(ccnum))) + 1;
    while (n <= nDigits)
    {
        //for the even position digits
        if (n % 2 == 0)
        {
            double position_a = fmod(ccnum, index);
            double index_minus = pow(10, n - 1);
            int digit_a = position_a / index_minus;
            double double_digit_a = 2 * digit_a;
            //split double digit numbers into its separate digits
            if (double_digit_a >= 10)
            {
                int one = fmod(double_digit_a, 10);
                int two = double_digit_a / 10;
                double_digit_a = one + two;
            }
            even_sum = double_digit_a + even_sum;
        }

        //for odd digits
        else if (n % 2 != 0)
        {
            double position_b = fmod(ccnum, index);
            double index_minus = pow(10, (n - 1));
            int digit_b = position_b / index_minus;
            odd_sum = digit_b + odd_sum;
        }

        n += 1;
        index = pow(10, n);
    }

    int final_sum = odd_sum + even_sum;

    if (final_sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;//breaks
    }

    if (final_sum % 10 == 0)
    {
        int first = ccnum / pow(10, nDigits - 2);
        printf("%i\n", first);
        //amex
        if ((first == 34 || first == 37) && nDigits == 15)
        {
            printf("AMEX\n");

        }
        //mastercard
        else if ((first == 51 || first == 52 || first == 53 || first == 54 || first == 55) && nDigits == 16)
        {
            printf("MASTERCARD\n");
        }
        //visa
        else if (first / 10 == 4 && (nDigits == 13 || nDigits == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

}
