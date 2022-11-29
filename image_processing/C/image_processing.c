#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> //For getcwd
#include <time.h>
#include <stdbool.h>

#define PATH_MAX    4096

struct Size {
    int rows, cols;
};

typedef struct Size Size;

//Lite oklart om denna funkar
void delete_arr(unsigned char** arr, Size size){

    for(int i = 0; i < size.rows; i++){
        free(arr[i]);
    }
    free(arr);
}

unsigned char** create_arr(Size size){

    //Ändra till malloc när allt funkar (Förutom den som padding kallar)

    //printf("Creating array with size: %dx%d\n", size.rows, size.cols);

    unsigned char** arr = calloc(size.rows, sizeof(char*));
    for(int i = 0; i < size.rows; i++){
        arr[i] = calloc(size.cols, sizeof(char));
    }

    return arr;
}

void export_csv(unsigned char** arr, Size arrsize, char fileName[]){
    
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
    fclose(csv);
}

void print_arr(unsigned char** arr, Size arrsize){

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

unsigned char** load_file(Size imsize, char fileName[]){

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));

    printf("Loading file \"%s\"...\n", strcat(cwd, fileName));
    printf("cwd = %s\n", cwd);
    
    FILE *fptr = fopen(cwd, "r");

    if ( fptr == NULL ){
        printf("File open error..\n");
        exit(-1);
    }

    unsigned char** image_matrix = create_arr(imsize);

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

unsigned char** pad(unsigned char** image, Size *imsize){

    //Update imsize and allocate new expanded array
    imsize->rows += 2;
    imsize->cols += 2;
    unsigned char** expanded = create_arr(*imsize);

    for(int i = 0; i < imsize->rows - 2; i++){
        memcpy(&expanded[i + 1][1], image[i], (size_t)(imsize->cols*sizeof(char) - 2));
    }

    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return expanded;
}

unsigned char** unpad(unsigned char** image, Size *imsize){

    imsize->rows -= 2;
    imsize->cols -= 2;
    unsigned char** reduced = create_arr(*imsize);

    for(int i = 0; i < imsize->rows; i++){
        memcpy(reduced[i], &image[i + 1][1], imsize->cols*sizeof(char));
    }

    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return reduced;
}

unsigned char** subarray(Size ker_size, unsigned char** image, int row, int col){

    unsigned char** sub = create_arr(ker_size);
    
    for(int i = 0; i < ker_size.rows; i++){
        memcpy(sub[i], &image[row + i - 1][col - 1], ker_size.cols*sizeof(char));
    }

    return sub;
}

// int** sobel(int** image, Size imsize, Size kernelsize){

//     int h[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1 ,0, 1}};
//     //int h[3][3] = {{1, 0, -1}, {2, 0, -2}, {1 ,0, -1}};

//     int** sobeld = create_arr(imsize);
//     int ** sub;
//     int S1 = 0;
//     for(int i = 1; i < imsize.rows-1; i++)
//     {
//         for(int j = 1; j < imsize.cols-1; j++)
//         {
//             sub = subarray(kernelsize, image, i, j);

//             //Calculate total value over kernel
//             for(int p = 0; p < kernelsize.rows; p++)
//             {
//                 for(int q = 0; q < kernelsize.cols; q++)
//                 {
//                     S1 += h[p][q] * sub[p][q];
//                 }
//             }
//             S1 = (int)(abs(S1)/4);
//             sobeld[i][j] = S1;
//             S1 = 0;
//         }
//     }
//     //Oklart om vi ska göra en free här
//     //delete_arr(image);
//     return sobeld;
// }

unsigned char** sobel(unsigned char** image, Size imsize, Size kernelsize, bool xy){

    unsigned char** sobeld = create_arr(imsize);
    int x = 0;
    int y = 0;

    for(int i = 1; i < imsize.rows-1; i++)
    {
        for(int j = 1; j < imsize.cols-1; j++)
        {
            x = -0.25*(image[i - 1][j - 1] + image[i + 1][j - 1]) + image[i - 1][j + 1] + image[i + 1][j + 1] + 2*(image[i][j + 1] - image[i][j - 1]);
            if(xy){
                y = -0.25*(image[i + 1][j - 1] + image[i + 1][j + 1]) + image[i - 1][j - 1] + image[i - 1][j + 1] + 2*(image[i - 1][j] - image[i + 1][j]);
                sobeld[i][j] = (unsigned char) (abs(x) + abs(y));
            }
            else{
                sobeld[i][j] = (unsigned char) (abs(x));
            }
        }
    }
    
    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return sobeld;
}

unsigned char** threshold(unsigned char** image, Size imsize, Size kernelsize, int offset){

    unsigned char** thresholded = create_arr(imsize);
    int mean;

    for(int i = 1; i < imsize.rows - 1; i++){
        for(int j = 1; j < imsize.cols - 1; j++){

            //0.1 pga ungefär /9
            mean = 0.1*(image[i-1][j-1] + image[i-1][j] + image[i-1][j+1] + image[i][j-1] + image[i][j] + image[i][j+1] + image[i+1][j-1] + image[i+1][j] + image[i+1][j+1]); 

            thresholded[i][j] = (unsigned char) ((image[i][j] < ( mean - offset )) ? 255 : 0);
            mean = 0;
        }
    }
    //Gamla threshold
    //  sub = subarray(kernelsize, image, i, j);

    //         //Calculate mean
    //         for(int p = 0; p < kernelsize.rows; p++){
    //             for(int q = 0; q < kernelsize.rows; q++){
                    
    //                 mean += sub[p][q];

    //                 if(p == kernelsize.rows - 1 && q == kernelsize.cols - 1){
    //                     mean = (int) mean/(p*q);
    //                 }
    //             }
    //         }

    //Oklart om vi ska göra en free här
    //delete_arr(image);
    return thresholded;
}

unsigned char** diff(unsigned char** ref, unsigned char** test, Size imsize){

    unsigned char** difference = create_arr(imsize);
    for(int i = 0; i < imsize.rows; i++){
        for(int j = 0; j < imsize.cols; j++){
            difference[i][j] = (unsigned char) abs(ref[i][j] - test[i][j]);
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
    unsigned char** image;

    image = load_file(imsize, "/numbers.csv");
    image = pad(image, &imsize);
    image = sobel(image, imsize, kernelsize, true);
    image = threshold(image, imsize, kernelsize, 20);
    image = unpad(image, &imsize);

    elapsed_time = ((double) (clock() - start) / CLOCKS_PER_SEC);

    print_arr(image, imsize);
    export_csv(image, imsize, "output.csv");

    if((int)elapsed_time > 0){
        printf("Execution time: %.3fs\n", elapsed_time);
    }
    else if((int)(elapsed_time*1000) > 0){
        printf("Execution time: %.3fms\n", 1000*elapsed_time);
    }
    else{
        printf("Execution time: %.3fus\n", 1000000*elapsed_time);
    }
    
    //"delete_arr" funkar inte ibland, tror vi råkar allokera på stacken istället för heapen, men fattar inte riktigt (man ska/kan inte free:a på stacken)
    if(image != NULL){
        delete_arr(image, imsize);
    }

    return 0;
}