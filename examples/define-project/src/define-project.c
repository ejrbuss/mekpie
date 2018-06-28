#include <stdio.h>
#include <stdlib.h>

int main() {
    // By default all projects are provided a version
    printf("Currently running with v%s!\n", VERSION);
    // Any values provided to the define config section are accessible
    printf("I was given the secret: %d\n", SECRET);
    // And names are defined/undefined as configured
    #ifdef DEBUG
    puts("DEBUG!");
    #elif RELEASE
    puts("RELEASE");
    #endif
    puts("Hello, World!");
    return EXIT_SUCCESS;
}
