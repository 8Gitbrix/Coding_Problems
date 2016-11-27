#include <stdio.h>
#include <stdlib.h>

int main(){
      int val = 0x354c;
      int k =ADDi(val,0,3);
      printf("bit is: %d", k);
}
int ADDi(int val, int left, int right){
	int m = right-left+1;
	int p = 15-right;
	int mask = ((1<<m)-1)<<p; //mask of 0s, m 1s, and p 0s
	int result = val & mask;
	result = result >> p; //right shift the result so your copied bits start at index 0
	return result;
}
