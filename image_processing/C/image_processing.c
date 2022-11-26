#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> //For getcwd

#define PATH_MAX    4096

struct Size {
    int rows, cols;
};

typedef struct Size Size;

int** create_arr(Size size){

    printf("Creating array with size: %dx%d\n", size.rows, size.cols);

    int** arr = calloc(size.rows, sizeof(int*));
    for(int i = 0; i < size.rows; i++){
        arr[i] = calloc(size.cols, sizeof(int));
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
                printf("%d ", arr[i][j]);
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

int** load_file(Size imsize, char fileName[]){

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));

    printf("Loading file \"%s\"...\n", strcat(cwd, fileName));
    printf("cwd = %s\n", cwd);
    
    FILE *fptr = fopen(cwd, "r");

    if ( fptr == NULL ){
        printf("File open error..\n");
        exit(-1);
    }

    int** image_matrix = create_arr(imsize);

    int i = 0;
    int j = 0;
    int number;

    //Load all integers from the csv
    while ( fscanf(fptr, "%d", &number) != EOF ){

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

    return image_matrix;
}

int** pad(int** image, Size *imsize){

    //Update imsize and allocate new expanded array
    imsize->rows += 2;
    imsize->cols += 2;
    int** expanded = create_arr(*imsize);
    int* ad;

    for(int i = 0; i < imsize->rows - 2; i++){
        ad = &expanded[i+1][1];
        memcpy(ad, image[i], (size_t)(imsize->cols*sizeof(int) - 2));
    }

    free(image);
    return expanded;
}

int** unpad(int** image, Size *imsize){

    imsize->rows -= 2;
    imsize->cols -= 2;
    int** reduced = create_arr(*imsize);
    int* ad;

    for(int i = 0; i < imsize->rows; i++){
        ad = &image[i + 1][1];
        memcpy(reduced[i], ad, imsize->cols*sizeof(int));
    }

    free(image);
    return reduced;
}

int main(int argc, char **argv){

    Size imsize = { .rows = 200, .cols = 200 };
    int** image;

    image = load_file(imsize, "/numbers.csv"); //Oklart om denna bör initiera image arrayen eller om man ska göra det utanför, funkar iaf.
    image = pad(image, &imsize);
    image = unpad(image, &imsize);
    print_arr(image, imsize);

    export_csv(image, imsize, "output.csv");

    free(image);
    return 0;
}