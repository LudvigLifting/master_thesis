#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> //For getcwd
#include <time.h>

#define PATH_MAX    4096

struct Size {
    int rows, cols;
};

typedef struct Size Size;

//Lite oklart om denna funkar
void delete_arr(int** arr, Size size){

    for(int i = 0; i < size.rows; i++){
        free(arr[i]);
    }
    free(arr);
}

int** create_arr(Size size){

    //Ändra till malloc när allt funkar

    //printf("Creating array with size: %dx%d\n", size.rows, size.cols);

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

        if( i > imsize.rows-1 ){
            //Matrix full
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
    //delete_arr(image);
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
    //delete_arr(image);
    return reduced;
}

int** subarray(Size ker_size, int** image, int row, int col){

    int** sub = create_arr(ker_size);
    
    for(int i = 0; i < ker_size.rows; i++){
        memcpy(sub[i], &image[row + i - 1][col - 1], ker_size.cols*sizeof(int));
    }

    return sub;
}

int** sobel(int** image, Size imsize, Size kernelsize){

    int Gx[3][3] = {{1, 0, -1}, {2, 0, -2}, {1 ,0, -1}};

    int** sobeld = create_arr(imsize);
    int ** sub;
    int S1;
    for(int i = 1; i < imsize.rows-1; i++)
    {
        for(int j = 1; j < imsize.cols-1; j++)
        {
            sub = subarray(kernelsize, image, i, j);

            //Calculate total value over kernel
            for(int p = 0; p < kernelsize.rows; p++)
            {
                for(int l = 0; l < kernelsize.cols; l++)
                {
                    for(int q = 0; q < kernelsize.rows; q++)
                    {                    
                        S1 += Gx[p][q] * sub[q][l];
                    }
                }
            }
            S1 = (int)(abs(S1)/12);
            sobeld[i][j] = S1;
            S1 = 0;
        }
    }
    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return sobeld;
}

int** threshold(int** image, Size imsize, Size kernelsize, int offset){

    int** thresholded = create_arr(imsize);
    int** sub;
    int mean;

    for(int i = 1; i < imsize.rows - 1; i++){
        for(int j = 1; j < imsize.cols - 1; j++){

            sub = subarray(kernelsize, image, i, j);

            //Calculate mean
            for(int p = 0; p < kernelsize.rows; p++){
                for(int q = 0; q < kernelsize.rows; q++){
                    
                    mean += sub[p][q];

                    if(p == kernelsize.rows - 1 && q == kernelsize.cols - 1){
                        mean = (int) mean/(p*q);
                    }
                }
            }

            thresholded[i][j] = (image[i][j] < ( mean - offset )) ? 255 : 0;
            mean = 0;
        }
    }

    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return thresholded;
}

int** diff(int** ref, int** test, Size imsize){

    int** difference = create_arr(imsize);
    for(int i = 0; i < imsize.rows; i++){
        for(int j = 0; j < imsize.cols; j++){
            difference[i][j] = abs(ref[i][j] - test[i][j]);
        }
    }
    
    //Oklart om vi ska göra en free här
    //delete_arr(test);
    return difference;
}


int main(int argc, char **argv){

    clock_t start;
    double elapsed_time;

    start = clock();

    Size imsize = { .rows = 200, .cols = 200 };
    Size kernelsize = { .rows = 3, .cols = 3 };
    int** image;

    image = load_file(imsize, "/numbers.csv");
    image = pad(image, &imsize);

    image = sobel(image, imsize, kernelsize);
    //image = threshold(image, imsize, kernelsize, 30);
    image = unpad(image, &imsize);

    // SOBEL TEST //
    Size lolsize = { .rows = 9, .cols = 9 };
    int** test = create_arr(lolsize);
    int lol[9][9] = {{163, 151, 162, 85, 83, 190, 241, 252, 249},
            {121, 107, 82, 20, 19, 233, 226, 45, 81},
            {142, 31, 86, 8, 87, 39, 167, 5, 212},
            {208, 82, 130, 119, 117, 27, 153, 74, 237},
            {88, 61, 106, 82, 54, 213, 36, 74, 104},
            {142, 173, 149, 95, 60, 53, 181, 196, 140},
            {221, 108, 17, 50, 61, 226, 180, 180, 89},
            {207, 206, 35, 61, 39, 223, 167, 249, 150},
            {252, 30, 224, 102, 44, 14, 123, 140, 202}};
    for(int i = 0; i < lolsize.rows; i++){
        for(int j = 0; j < lolsize.cols; j++){
            test[i][j] = lol[i][j];
        }
    }
    test = pad(test, &lolsize);
    test = sobel(test, lolsize, kernelsize);
    test = unpad(test, &lolsize);
    print_arr(test, lolsize);
    // SOBEL TEST //

    //export_csv(image, imsize, "output.csv");

    elapsed_time = ((double) (clock() - start) / CLOCKS_PER_SEC);
    printf("Execution time: %fs\n", elapsed_time);

    //"delete_arr" funkar inte ibland, tror vi råkar allokera på stacken istället för heapen, men fattar inte riktigt (man ska/kan inte free:a på stacken)
    // if(image != NULL){
    //     delete_arr(image, imsize);
    // }

    return 0;
}