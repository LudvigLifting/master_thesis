#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> //For getcwd
#include <time.h>
#include <stdbool.h>
#include <errno.h>

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

unsigned char** create_arr(Size size, bool mal){

    //printf("Creating array with size: %dx%d\n", size.rows, size.cols);

    unsigned char** arr;

    if(mal){
        arr = malloc(size.rows * sizeof(char*));
        for(int i = 0; i < size.rows; i++){

            arr[i] = malloc(size.cols * sizeof(char));
    }
    }
    else{
        arr = calloc(size.rows, sizeof(char*));
        for(int i = 0; i < size.rows; i++){

            arr[i] = calloc(size.cols, sizeof(char));
        }
    }

    return arr;
}

void export_csv(unsigned char** arr, Size arrsize, char fileName[]){

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));
    strcat(cwd, fileName);
    printf("Exporting file \"%s\"\n...\n", cwd);
    
    FILE *csv = fopen(cwd, "w");
    
    if( csv == NULL ){
        printf("Export: file open error.. %s\n", strerror(errno));
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
    strcat(cwd, fileName);

    printf("Loading file \"%s\"\n...\n", cwd);
    
    FILE *fptr = fopen(cwd, "r");

    if ( fptr == NULL ){
        printf("Load: File open error..(%s)\n", strerror(errno));
        exit(-1);
    }

    unsigned char** image_matrix = create_arr(imsize, true);

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
    Size newSize = { .rows = imsize->rows + 2, .cols = imsize->cols + 2 };
    unsigned char** expanded = create_arr(newSize, false);

    for(int i = 0; i < imsize->rows; i++){

        memcpy(&expanded[i + 1][1], image[i], (size_t)(imsize->cols*sizeof(char)));
    }

    delete_arr(image, *imsize);
    imsize->rows += 2;
    imsize->cols += 2;

    return expanded;
}

unsigned char** unpad(unsigned char** image, Size *imsize){

    Size newSize = { .rows = imsize->rows - 2, .cols = imsize->cols - 2 };
    unsigned char** reduced = create_arr(newSize, false);

    for(int i = 0; i < newSize.rows; i++){

        memcpy(reduced[i], &image[i + 1][1], newSize.cols*sizeof(char));
    }

    delete_arr(image, *imsize);
    imsize->rows -= 2;
    imsize->cols -= 2;

    return reduced;
}

unsigned char** sobel(unsigned char** image, Size imsize, bool xy){

    unsigned char** sobeld = create_arr(imsize, true);
    int x = 0;
    int y = 0;

    for(int i = 1; i < imsize.rows-1; i++){
        for(int j = 1; j < imsize.cols-1; j++){

            x = 0.25*(-(image[i - 1][j - 1] + image[i + 1][j - 1]) + image[i - 1][j + 1] + image[i + 1][j + 1] + 2*(image[i][j + 1] - image[i][j - 1]));
            if(xy){
                y = 0.25*(-(image[i + 1][j - 1] + image[i + 1][j + 1]) + image[i - 1][j - 1] + image[i - 1][j + 1] + 2*(image[i - 1][j] - image[i + 1][j]));
                sobeld[i][j] = (unsigned char) (abs(x) + abs(y));
            }
            else{
                sobeld[i][j] = (unsigned char) (abs(x));
            }
        }
    }
    
    delete_arr(image, imsize);
    return sobeld;
}

unsigned char** threshold(unsigned char** image, Size imsize, int offset){

    unsigned char** thresholded = create_arr(imsize, true);
    int mean;

    for(int i = 1; i < imsize.rows - 1; i++){
        for(int j = 1; j < imsize.cols - 1; j++){

            mean = 0.125*(image[i-1][j-1] + image[i-1][j] + image[i-1][j+1] + image[i][j-1] + image[i][j+1] + image[i+1][j-1] + image[i+1][j] + image[i+1][j+1]);

            thresholded[i][j] = (unsigned char) ((image[i][j] < ( mean - offset )) ? 255 : 0);
            mean = 0;
        }
    }

    delete_arr(image, imsize);
    return thresholded;
}

unsigned char** diff(unsigned char** ref, unsigned char** test, Size imsize){

    unsigned char** difference = create_arr(imsize, true);
    for(int i = 0; i < imsize.rows; i++){
        for(int j = 0; j < imsize.cols; j++){

            difference[i][j] = (unsigned char) abs(ref[i][j] - test[i][j]);
        }
    }
    
    return difference;
}

unsigned char** filter_dots(unsigned char** image, Size size){

    unsigned char** filtered = create_arr(size, false);
    int sum = 0;

    for(int i = 1; i < size.rows - 1; i++){
        for(int j = 1; j < size.cols - 1; j++){
            
            if(image[i][j] < 255){
                //Nodot
                filtered[i][j] = image[i][j];
            }
            else{
                //dot
                sum = image[i-1][j-1] + image[i-1][j] + image[i-1][j+1] + image[i][j-1] + image[i][j+1] + image[i+1][j-1] + image[i+1][j] + image[i+1][j+1];
                if(sum <= 255){
                    //unimportant dot
                    filtered[i][j] = 0;                    
                }
                else{
                    //important dot
                    filtered[i][j] = image[i][j];
                }
            }
        }
    }

    delete_arr(image, size);
    return filtered; 
}

bool decide(unsigned char** diff, Size size, int floor){

    int nbr = 0;
    bool decide = false;

    //Count white pixels
    for(int i = 0; i < size.rows; i++){
        for(int j = 0; j < size.cols; j++){

            if(diff[i][j] > 0){
                nbr++;
            }
        }
    }

    if(nbr > floor){
        decide = true;
    }

    return decide;
}

bool process(char file[], char ref[], char output[]){

    Size imsize = { .rows = 200, .cols = 200 };
    unsigned char** reference;
    unsigned char** image;
    unsigned char** difference = create_arr(imsize, true);
    bool decision;
    int thresh_val = 5;

    //printf("File: %s\nReference: %s\nOutput: %s\n", file, ref, output);

    image = load_file(imsize, file);
    image = pad(image, &imsize);
    image = sobel(image, imsize, false);
    image = unpad(image, &imsize);
    //export_csv(image, imsize, "/figures/sobeled.csv");
    image = pad(image, &imsize);
    image = threshold(image, imsize, thresh_val);
    image = unpad(image, &imsize);
    //export_csv(image, imsize, "/figures/thresholded.csv");

    reference = load_file(imsize, ref);
    reference = pad(reference, &imsize);
    reference = sobel(reference, imsize, false);
    reference = threshold(reference, imsize, thresh_val);
    reference = unpad(reference, &imsize);
    //export_csv(reference, imsize, "/figures/reference.csv");

    difference = diff(reference, image, imsize);
    //export_csv(difference, imsize, "/figures/diff_unfiltered.csv");
    difference = pad(difference, &imsize);
    difference = filter_dots(difference, imsize);
    difference = unpad(difference, &imsize);
    decision = decide(difference, imsize, 280);
    //printf("Decision is: %d\n", decision);

    export_csv(difference, imsize, output);
    
    if(image != NULL){
        delete_arr(image, imsize);
    }

    return decision;
}

int main(int argc, char** argv){

    clock_t start;
    double elapsed_time;

    start = clock();

    //CODE HERE//
    process(argv[1], argv[2], argv[3]);

    elapsed_time = ((double) (clock() - start) / CLOCKS_PER_SEC);

    if((int)elapsed_time > 0){
        printf("Execution time: %.3fs\n", elapsed_time);
    }
    else if((int)(elapsed_time*1000) > 0){
        printf("Execution time: %.3fms\n", 1000*elapsed_time);
    }
    else{
        printf("Execution time: %.3fus\n", 1000000*elapsed_time);
    }

    return 0;
}