#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>

struct Size {
    int height, width;
};

typedef struct Size Size;

int** create_arr(int N, int M){

    int **arr = calloc(N, sizeof(int));
    for(int i = 0; i < N; i++){
        arr[i] = calloc(M, sizeof(int));
    }

    return arr;
}

int main(void){

    Size image_size = { .height = 200, .width = 200 };

    int** image = create_arr(image_size.height, image_size.width);

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));
    char fileName[] = "/../python/huffman_coding/numbers.csv";

    FILE *fptr;

    //Get file handle
    fptr = fopen(strcat(cwd, fileName), "r");

    if (fptr == NULL){
        printf("File open error..\n");
        exit(-1);
    }

    int i, j = 0;
    int number;

    //Load image
    while ( fscanf(fptr, "%d", &number) == 1 ){

        if(i > 199){
            break;
        }

        image[i][j] = number;

        if(j != 0 && j % (image_size.width-1) == 0){
            i++;
            j = 0;
        }
        j++;
    }
    fclose(fptr);

    for(i = 0; i < image_size.height; i++){
        for(j = 0; j < image_size.width; j++){
            printf("%d ", image[i][j]);
        }
    }


    return 0;
}