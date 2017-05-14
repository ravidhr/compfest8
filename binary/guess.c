#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win_message(){
	printf("You win\nTo get the flag enter the password: ");
	
	char dummy_flag_filename[16] = "dummy_flag.txt";
	char real_flag_filename[16] = "real_flag.txt";

	char pass_filename[16] = "pass.txt";
	char password[16];
	gets(password);
	
	FILE * pass = fopen(pass_filename,"r");
	char real_password[16];
	if(pass){
		fread(real_password,1,15,pass);
		real_password[15] = 0;
	} else {
		printf("File not found\n");
		return;
	}

	if(strcmp(password, real_password) == 0){
		FILE * rf = fopen(real_flag_filename,"r");
		if(rf){
			char real_flag[64];
			fread(real_flag,1,63,rf);
			real_flag[63] = 0;
			printf("%s\n", real_flag);
		} else {
			printf("File not found\n");
			return;
		}
	} else {
		FILE * df = fopen(dummy_flag_filename,"r");
		if(df){
			char dummy_flag[64];
			fread(dummy_flag,1,63,df);
			dummy_flag[63] = 0;
			printf("%s\n", dummy_flag);
		} else {
			printf("File not found\n");
			return;
		}
	}
}

int min, max, mid, c;

int main(){
	min = 0;
	max = 1023;
	c = 0;
	const int MAXATT = 9;

	printf("Think of a number 0~1023, I can guess it with 10 questions or less\n\nAnswer with YES or NO:\n");

	char in[5];
	while(1){
		if(c > MAXATT){
			win_message();
			break;
		}

		mid = ((min+max)/2) + ((min+max)&1);
		printf("Is it less than %d?\n",mid);
		gets(in);

		if(strlen(in) == 3 && strncmp(in,"YES",3) == 0){
			max = mid-1;
		} else if (strlen(in) == 2 &&  strncmp(in,"NO",2) == 0){
			min = mid;
		} else{	
			printf("Invalid input\n");
			continue;
		}

		if(min==max){
			printf("Your number is: %d\n",min);
			break;
		}
		c++;
	}

return 0;
}