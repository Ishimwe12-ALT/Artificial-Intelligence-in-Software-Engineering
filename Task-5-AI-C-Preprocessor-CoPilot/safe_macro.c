#include <stdio.h>

/*
 * Safe macro: uses parentheses to avoid precedence issues
 */
#define MULTIPLY(a, b) ((a) * (b))

int main() {
    int result1 = MULTIPLY(2 + 3, 4);   // Correct: 20
    int result2 = MULTIPLY(5, 2 + 2);   // Correct: 20

    printf("Safe Result 1: %d\n", result1);
    printf("Safe Result 2: %d\n", result2);

    return 0;
}
