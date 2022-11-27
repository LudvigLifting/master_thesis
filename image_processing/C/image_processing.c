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

    //Ändra till malloc när allt funkar

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
            printf("\n ");
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

    for(int i = 0; i < imsize->rows - 2; i++){
        memcpy(&expanded[i + 1][1], image[i], (size_t)(imsize->cols*sizeof(int) - 2));
    }

    //Oklart om vi ska göra en free här
    free(image);
    return expanded;
}

int** unpad(int** image, Size *imsize){

    imsize->rows -= 2;
    imsize->cols -= 2;
    int** reduced = create_arr(*imsize);

    for(int i = 0; i < imsize->rows; i++){
        memcpy(reduced[i], &image[i + 1][1], imsize->cols*sizeof(int));
    }

    //Oklart om vi ska göra en free här
    free(image);
    return reduced;
}

int** subarray(Size ker_size, int** image, int row, int col){

    int** sub = create_arr(ker_size);
    
    for(int i = 0; i < ker_size.rows; i++){
        memcpy(sub[i], &image[row + i - 1][col - 1], ker_size.cols*sizeof(int));
    }

    return sub;
}

int** sobel(int** image, Size imsize){

    int** sobeld = create_arr(imsize);

    //Oklart om vi ska göra en free här
    free(image);
    return sobeld;
}

int** threshold(int** image, Size imsize, Size kernelsize, int offset){

    int** thresholded = create_arr(imsize);
    int** sub;
    int mean;

    for(int i = 0; i < imsize.rows; i++){
        for(int j = 0; j < imsize.cols; i++){

            sub = subarray(kernelsize, image, i, j);

            //Calculate mean
            for(int p = 0; p < kernelsize.rows; p++){
                for(int q = 0; q < kernelsize.rows; q++){
                    
                    mean += sub[p][q];

                    if(p == kernelsize.rows - 1 && q == kernelsize.cols - 1){
                        mean = (int) mean/(p*q); //Lite oklart hur vi ska göra med avrundning, om man castar så avrundas det alltid neråt, finns en round funktion i math.h
                    }
                }
            }

            thresholded[i][j] = (image[i][j] > mean) ? 255 : 0;
            mean = 0;
        }
    }

    //Oklart om vi ska göra en free här
    free(image);
    return thresholded;
}

int** diff(int** ref, int** test, Size imsize){

    int** difference = create_arr(imsize);
    for(int i = 0; i < imsize.rows; i++){
        for(int j = 0; j < imsize.cols; i++){
            difference[i][j] = abs(ref[i][j] - test[i][j]);
        }
    }
    
    //Oklart om vi ska göra en free här
    free(test);
    return difference;
}

int main(int argc, char **argv){

    Size imsize = { .rows = 200, .cols = 200 };
    Size kernelsize = { .rows = 3, .cols = 3 };
    int** image;

    image = load_file(imsize, "/numbers.csv");
    image = pad(image, &imsize);
    image = unpad(image, &imsize);

    export_csv(image, imsize, "output.csv");
    image = pad(image, &imsize);
    print_arr(image, imsize);
    int** sub = subarray(kernelsize, image, 200, 200);
    print_arr(sub, kernelsize);
    //print_arr(sub, kernelsize);

    if(image != NULL){
        free(image);
    }

    return 0;
}