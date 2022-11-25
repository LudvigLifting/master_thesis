#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>

#define PATH_MAX    4096

struct Size {
    int rows, cols;
};

typedef struct Size Size;

int** create_arr(int N, int M){

    int** arr = calloc(N, sizeof(int*));
    for(int i = 0; i < N; i++){
        arr[i] = calloc(M, sizeof(int));
    }

    return arr;
}

void export_csv(int** arr, Size arrsize, char fileName[]){
    
    FILE *csv = fopen(fileName, "w");
    if( csv == NULL ){
        printf("File open error..\n");
        exit( -1 );
    }
    for(int i = 0; i < arrsize.rows; i++){
        for(int j = 0; j < arrsize.cols; j++){

            fprintf(csv, "%d", arr[i][j]);
            if( j < arrsize.cols - 1 ){
                fprintf(csv, " ");
            }else{
                fprintf(csv, "\n");
            }
        }
    }
}

void print_arr(int** arr, Size arrsize){

    printf("[");
    for(int i = 0; i < arrsize.rows; i++){
        printf("[");
        for(int j = 0; j < arrsize.cols; j++){
            
            if( j < arrsize.cols - 1 ){
                printf("%d, ", arr[i][j]);
            }
            else{
                printf("%d]", arr[i][j]);
            }
        }
        if( i < arrsize.rows - 1 ){
            printf("\n");
        }
    }
    printf("]\n");
}

void load_file(int** image_matrix, Size imsize, char fileName[]){

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));

    printf("Loading file \"%s\"...\n", strcat(cwd, fileName));
    printf("cwd = %s\n", cwd);
    
    FILE *fptr = fopen(cwd, "r");

    if ( fptr == NULL ){
        printf("File open error..\n");
        exit(-1);
    }

    int i, j = 0;
    int number;

    //Load all integers from the csv
    while ( fscanf(fptr, "%d", &number) == 1 ){

        printf("Number i=%d, j=%d: %d\n", i, j, number);

        //Matrix full
        if( i > imsize.rows-1 ){
            break;
        }
        image_matrix[i][j] = number;

        if( j != 0 && j % ( imsize.cols - 1 ) == 0 ){
            //New row
            i++;
            j = 0;
        }else{
            j++;
        }
    }

    fclose(fptr);
}

void zero_padding(int** image, Size imsize){

}

int main(int argc, char **argv){

    Size imsize = { .rows = 200, .cols = 200 };

    int** image = create_arr(imsize.rows, imsize.cols);

    
    //Fett oklart försöker läsa numbers.csv från C-directoryt men får bara nollor, det enda som funkar är denna pathen till en annan mapp
    load_file(image, imsize, "/numbers.csv");
    //print_arr(image, imsize);

    // //Get file handle
    // FILE *fptr = fopen(strcat(cwd, fileName), "r");

    // if ( fptr == NULL ){
    //     printf("File open error..\n");
    //     exit(-1);
    // }

    // int i, j = 0;
    // int number;

    // //Load image
    // while ( fscanf(fptr, "%d", &number) == 1 ){

    //     if( i > imsize.rows-1 ){
    //         break;
    //     }
    //     image[i][j] = number;

    //     if( j != 0 && j % ( imsize.cols - 1 ) == 0 ){
    //         //New row
    //         i++;
    //         j = 0;
    //     }else{
    //         j++;
    //     }
    // }

    // fclose(fptr);

    //print_arr(image, imsize);

    export_csv(image, imsize, "output.csv");

    free(image);
    return 0;
}