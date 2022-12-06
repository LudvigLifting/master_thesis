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
    
    FILE *csv = fopen(fileName, "w");
    if( csv == NULL ){
        printf("File open error.. %s\n", strerror(errno));
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

    printf("Loading file \"%s\"\n...\n", strcat(cwd, fileName));
    
    FILE *fptr = fopen(cwd, "r");

    if ( fptr == NULL ){
        printf("File open error..\n");
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
    imsize->rows += 2;
    imsize->cols += 2;
    unsigned char** expanded = create_arr(*imsize, false); //calloc här, kanske är snabbare att köra malloc och sen manuellt lägga till nollor

    for(int i = 0; i < imsize->rows - 2; i++){

        memcpy(&expanded[i + 1][1], image[i], (size_t)(imsize->cols*sizeof(char) - 2));
    }

    //Oklart om vi ska göra en free här
    // Size size = { .rows=imsize->rows, .cols=imsize->cols };
    // delete_arr(image, size);
    return expanded;
}

unsigned char** unpad(unsigned char** image, Size *imsize){

    imsize->rows -= 2;
    imsize->cols -= 2;
    unsigned char** reduced = create_arr(*imsize, false);

    for(int i = 0; i < imsize->rows; i++){

        memcpy(reduced[i], &image[i + 1][1], imsize->cols*sizeof(char));
    }

    //Oklart om vi ska göra en free här
    // Size size = { .rows=imsize->rows, .cols=imsize->cols };
    // delete_arr(image, size);
    return reduced;
}

//Kanske inte behövs alls, blir typ 3ggr så långsamt med en algoritm + subarray
unsigned char** subarray(Size ker_size, unsigned char** image, int row, int col){

    unsigned char** sub = create_arr(ker_size, true);
    
    for(int i = 0; i < ker_size.rows; i++){

        memcpy(sub[i], &image[row + i - 1][col - 1], ker_size.cols*sizeof(char));
    }

    return sub;
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
    
    //Oklart om vi ska göra en free här
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

    //Oklart om vi ska göra en free här
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
    
    //Oklart om vi ska göra en free här
    //delete_arr(test);
    return difference;
}

//Om vi ska ha detta
int calc_floor(unsigned char** diff, Size size){
    
    int mean = 0;
    for(int i = 0; i < size.rows; i++){
        for(int j = 0; j < size.cols; j++){

            mean += diff[i][j];
        }
    }

    return (int)(mean/(size.rows * size.cols));
}

bool decision(unsigned char** diff, Size size, int floor){

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

void process(char file[], char output[]){

    Size imsize = { .rows = 200, .cols = 200 };
    unsigned char** image = create_arr(imsize, true);

    image = load_file(imsize, file);
    image = pad(image, &imsize);
    image = sobel(image, imsize, false);
    image = threshold(image, imsize, 5);
    image = unpad(image, &imsize);

    export_csv(image, imsize, output);
}

void many_images(){

    char file[13] = "/many/";
    char out[12] = "/out/";

    for(int i = 0; i < 100; i++){

        sprintf(&file[6], "%d", i);
        sprintf(&out[5], "%d", i);
        strcat(file, ".csv");
        strcat(out, ".csv");

        process(file, out);

        file[6] = '\0';
        out[5] = '\0';
    }
}

int main(int argc, char **argv){

    many_images();
    return 0;

    clock_t start;
    double elapsed_time;

    start = clock();

    Size imsize = { .rows = 200, .cols = 200 };
    unsigned char** image;

    image = load_file(imsize, "/numbers.csv");
    image = pad(image, &imsize);
    image = sobel(image, imsize, false);
    image = threshold(image, imsize, 5);
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
    
    if(image != NULL){
        delete_arr(image, imsize);
    }

    return 0;
}