#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Size {
    int height, width;
};

typedef struct Size Size;

Size get_image_size(char* fileName){

    Size size;
    char temp[4];
    
    strncpy(temp, fileName + 10, 3);
    temp[3] = '\0';
    size.width = atoi(temp);

    strncpy(temp, fileName + 14, 3);
    temp[3] = '\0';
    size.height = atoi(temp);

    return size;
}

int main(void){

    printf("\n");
    FILE *fptr;
    char path[100] = "../pictures/";
    char fileName[] = "test_color100x100.jpg";
    Size size = calcSize(fileName);

    printf("Image: width = %d, height = %d\n", size.width, size.height);

    printf("concat = %s\n", strcat(path, fileName));

    fptr = fopen(fileName, "r");

    if (fptr == NULL){
        printf("File open error..\n");
        exit(-1);
    }

    char number;
    char *arr[100];
    int i = 0;

    while ( fscanf(fptr, "%c", & number ) == 1 ){ 
        
        int arr_size = sizeof(arr)/sizeof(char);
        if(i >= arr_size){

            char temp[arr_size + 100*sizeof(char)];
            memcpy(temp, arr, arr_size);
            arr = temp;
            free(temp);
        }
        arr[i] = number; 
        i++;
    } 

    return 0;
}