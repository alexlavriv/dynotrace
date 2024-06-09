#include <stdio.h>
void print(int k){
	printf("test %d\n", k);
}

int main(){
  FILE *fptr;

  // Create a file on your computer (filename.txt)
  fptr = fopen("filename.txt", "w");

  // Close the file
  fclose(fptr);
  	printf("Enter num:\n");
	int num;
	scanf("%d", &num);
	for (int i = 0; i < num; i++){
		print(i);
	}
	return 0;
}
