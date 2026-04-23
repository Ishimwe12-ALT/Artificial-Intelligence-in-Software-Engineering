#include <stdio.h>

/*
 * Flawed macro: missing parentheses → operator precedence bug
 */
#define MULTIPLY(a, b) a * b

int main() {
    int result1 = MULTIPLY(2 + 3, 4);   // Expected: 20, Actual: 14
    int result2 = MULTIPLY(5, 2 + 2);   // Expected: 20, Actual: 12

    printf("Result 1: %d\n", result1);
    printf("Result 2: %d\n", result2);

    return 0;
}
