// Ashwin Jeyaseelan L02
// CS 350, Fall 2015
// LC-3 Simulator Phase 3

#include <stdio.h>
#include <stdlib.h>
#include <string.h> /* memset */

typedef short int Word;
typedef unsigned char Address;
#define MEMLEN 65536 //2^16
#define NREG 8

typedef struct {
	Word mem[MEMLEN];
	Word reg[NREG];      // Note: "register" is a reserved word
    int pc;               //Program Counter
	int running;         // running = 1 iff CPU is executing instructions
	int ir;             // Instruction Register //CHANGED FROM WORD TO INT!
    int opcode;          //   opcode field
	int reg_R;           //   register field
	int addr_MM;         //   memory field
	int cc;              // Condition Code
	int instr_sign;      // sign of instruction
} CPU;

int main(int argc, char *argv[]);
void initialize_CPU(CPU *cpu);
void initialize_memory(int argc, char *argv[], CPU *cpu, FILE *datafile);
FILE *get_datafile(int argc, char *argv[]);
void dump_CPU(CPU *cpu);
void dump_memory(CPU *cpu);
void dump_registers(CPU *cpu);

int read_execute_command(CPU *cpu);
int execute_command(char cmd_char,char c2, int val, int val2, CPU *cpu);
void help_message(void);
void many_instruction_cycles(int nbr_cycles, CPU *cpu);
void one_instruction_cycle(CPU *cpu);
void exec_HLT(CPU *cpu);

int copyBits(int val, int left, int right); //to copy bits of insturctions for LC3 functions //WORD CHANGE
void setCC(CPU *cpu, int val); //WORD CHANGE
int getCC(CPU *cpu);

//instructions to execute:
void BR(CPU *cpu);
void ADD(CPU *cpu);
void LD(CPU *cpu);
void ST(CPU *cpu);
void JSR(CPU *cpu);
void JSRR(CPU *cpu);
void AND(CPU *cpu);
void LDR(CPU *cpu);
void STR(CPU *cpu);
void RTI(CPU *cpu);
void NOT(CPU *cpu);
void LDI(CPU *cpu);
void STI(CPU *cpu);
void JMP(CPU *cpu);
void err(CPU *cpu);
void LEA(CPU *cpu);
void TRAP(CPU *cpu);

int main(int argc, char *argv[]) {
	CPU cpu_value, *cpu = &cpu_value;
	printf("Ashwin Jeyaseelan CS 350 L02 Final Project Phase 1\n");
	FILE *f = get_datafile(argc, argv);
	initialize_CPU(cpu);
	initialize_memory(argc,argv,cpu,f);
      dump_CPU(cpu);
      dump_memory(cpu);
	char *prompt = "> ";
	printf("\nBeginning execution; type h for help\n%s", prompt);

	int done = read_execute_command(cpu);
	while (!done) {
		printf("%s", prompt);
		done = read_execute_command(cpu);
	}
	return 0;
}
void initialize_CPU(CPU *cpu) {
	cpu -> pc = 0x0000;
	cpu -> ir =0x0000;
	cpu -> running = 1;
	cpu -> cc = 0;
	int i;
	for (i=0; i<NREG; i++) {
		cpu -> reg[i]=0;
	}
		//dump_CPU(cpu);
}
// Read initial values for memory
void initialize_memory(int argc, char *argv[], CPU *cpu, FILE *datafile) {
// Buffer to read next line of text into
	#define BUFFER_LEN 80
	char buffer[BUFFER_LEN];
	int value_read,loc, words_read,done = 0;
	char *read_success;    // NULL if reading in a line fails.
      int counter = 0; //used to keep track of the first line
      memset(cpu->mem,0,sizeof(cpu->mem)); //preset all values to 0 in mem array

	read_success = fgets(buffer, BUFFER_LEN, datafile);
	while (read_success != NULL && !done) {
		if(counter==0){ //if on the first line, set PC to that value
			words_read= sscanf(buffer,"%x",&value_read);
                  loc = value_read;
                  cpu -> pc = (unsigned short)loc;
            }
            else{
			words_read = sscanf(buffer, "%x", &value_read);
			if (words_read>0 && loc<MEMLEN &&counter!=0){
				if (loc==0xFFFF){
					loc = 0;
            	}
                    cpu->mem[loc] = value_read;
                    loc++;
                }
            }
		//Get the next line in the file:
		read_success = fgets(buffer, BUFFER_LEN, datafile);
            counter++;
	}
	fclose(datafile);
		//dump_memory(cpu);
}

FILE *get_datafile(int argc, char *argv[]) {
	char *datafile_name;
	if(argc !=2){
		datafile_name = "default.hex";
		printf("\nThe default file opened will be: default.hex\n");
	}
	else{
		datafile_name = argv[1];
	}
	printf("Loading %s\n",datafile_name);
	FILE *datafile = fopen(datafile_name, "r");

	if(datafile == NULL){
		printf("Failed to open file %s\n", datafile_name);
		exit(EXIT_FAILURE);
	}
	return datafile;
}
void dump_CPU(CPU *cpu) {
	char ccVal;
	if(cpu->cc == 0){
		ccVal ='Z';
	}
	if(cpu->cc > 0){
		ccVal = 'P';
	}
	if(cpu->cc < 0){
		ccVal = 'N';
	}
	printf("\nCONTROL UNIT:\n");
	printf("PC = x%04X", cpu ->pc);
	printf("   IR = x%04x", (*cpu).ir);
	printf("   CC = %c",ccVal);
	printf("   RUNNING: %d",(*cpu).running);
	dump_registers(cpu);
}
void dump_memory(CPU *cpu) {
	printf("\nMEMORY (addresses x0000 - xFFFF):\n");
	int i;
	for(i=0; i<MEMLEN;i++){
		if(cpu->mem[i]!=0){
			printf("x%04X:  x%04X\t%d \n",i,(unsigned short)cpu->mem[i],cpu->mem[i]);
		}
	}
      printf("\n");
}
void dump_registers(CPU *cpu) {
	printf("\n");
	int i;
	for(i=0;i<NREG;i++){
		if(i==4){
			//print a new line for the next 4 indices in register
			printf("\n");
		}
		printf("R%d x%04X %d   \t",i,(*cpu).reg[i],(*cpu).reg[i]);
	}
      printf("\n");
}
int read_execute_command(CPU *cpu) {
	// Buffer to read next command line into
	#define CMD_LINE_LEN 80
	char cmd_line[CMD_LINE_LEN];

	char *read_success;		// NULL if reading in a line fails.
	int nbr_cycles;		// Number of instruction cycles to execute
	char cmd_char;		// Command 'q', 'h', '?', 'd', or '\n'
	int done = 0;		// Should simulator stop?
	char c2;			// second char to handle the two types of s commands : "s rN x____ vs s x# x#...
	//to determine if second char is r v x?"
	int val;			// second values in commands such as g or s
	int val2;			// third value if s command s x# x#
	read_success = fgets(cmd_line, CMD_LINE_LEN, stdin);
	if ( !read_success ) {
		done = 1;   // Hit end of file
	}
	// else use sscanf on the cmd_buffer to read an integer nbr_cycles
	// if the sscanf succeeds, execute that many instruction cycles
	// else use sscanf on the cmd_buffer to read in a character cmd_char
	// ('q', 'h', '?', 'd', or '\n') and call execute_command on cmd_char
	else{
		int s;
		s = sscanf(cmd_line,"%d",&nbr_cycles);
		if(s==1){
			if(nbr_cycles==1){
				one_instruction_cycle(cpu);
			}
			else{
				many_instruction_cycles(nbr_cycles,cpu);
			}
		}
		else{
			//the first character of a command may be followed by a string that will be parsed into either 1 or two values
			//depending on the command  (.ie. set memory vs set register)
			sscanf(cmd_line,"%c %c%x x%x",&cmd_char,&c2,&val,&val2);
			execute_command(cmd_char,c2,val,val2,cpu);
		}
	}
	return done;
}
int execute_command(char cmd_char,char c2, int val, int val2, CPU *cpu) {
	if (cmd_char == '?' || cmd_char == 'h'|| cmd_char =='H') {
		help_message();
	}
	else if(cmd_char == 'q' || cmd_char=='Q'){
		printf("Quitting\n");
		exit(0);
	}
	else if(cmd_char == 'd' || cmd_char=='D'){
		dump_CPU(cpu);
		dump_memory(cpu);
	}
	else if(cmd_char == '\n'){
		if(cpu->running==0){
			one_instruction_cycle(cpu);
		}
		else{
			printf("\nCPU execution has halted\n");
		}
	}
	else if(cmd_char=='g'){
        int oldPc = cpu->pc;
		cpu -> pc = val;
		cpu -> running = 1;
        printf("The PC has been changed from %x to %x and running is now: %d \n",oldPc,val,cpu->running);
	}
	else if(cmd_char=='s'){
		// s rN xValue command
		if(c2=='r'){
			cpu -> reg[val]  = val2;
            printf("R%d = %x \n",val,val2);
		}
		// s xValue xValue command
		else{
			cpu -> mem[val] = val2;
            printf("M[%d] = %d\n",val,val2);
		}
	}
	return 0;
}

// Print standard message for simulator help command ('h' or '?')
//
void help_message(void) {
	printf("Command 'q'=quit, 'h' or '?'=help, 'd'= dump CPU contents\n");
	printf("s xAddress xValue: Set memory[address]<- value \n");
	printf("s rN xValue: Set register N <- value(N=0,...,7) \n");
	printf("integer: Execute that many instruction cycles \n");
	printf("(none: just the \\n): Execute 1 cycle \n");
}
void many_instruction_cycles(int nbr_cycles, CPU *cpu){
	if(nbr_cycles<1){
		printf("The number you entered is not valid");
		return;
	}
	//If the CPU isn't running, say so and return
	else if(cpu -> running==0){
		printf("\nCPU is not running");
		return;
	}
	else if(nbr_cycles>100){
		printf("The number of cycles entered is too large, we will use 100 instead");
		nbr_cycles = 100;
		int i;
		for(i=0;i<nbr_cycles;i++){
			one_instruction_cycle(cpu);
		}
	}
	else{
		int i;
		for(i=0;i<nbr_cycles;i++){
			one_instruction_cycle(cpu);
		}
	}
}
void one_instruction_cycle(CPU *cpu){
	if(cpu->running==0){
		//If the CPU isn't running, say so and return
		printf("CPU is not running anymore!\n");
		return;
	}
	// Get instruction and increment pc
	cpu -> ir = cpu -> mem[cpu -> pc];
	cpu ->pc = cpu->pc+1;
	// Decode instruction into opcode
    cpu -> opcode = copyBits(cpu->ir,0,3);

	// Echo instruction
	printf("\nIR: x%04x PC: x%04x \n",cpu->ir, cpu->pc);
    int ch;
	switch(cpu->opcode){
		case 0:
            BR(cpu);
            break;
		case 1: ADD(cpu); break;
		case 2: LD(cpu); break;
		case 3: ST(cpu); break;
		case 4:
			ch = copyBits(cpu->ir,4,4);
			if(ch==1)
				JSR(cpu);
			else
				JSRR(cpu);
			break;
		case 5: AND(cpu); break;
		case 6: LDR(cpu); break;
		case 7: STR(cpu); break;
		case 8: RTI(cpu); break;
		case 9: NOT(cpu); break;
		case 10: LDI(cpu); break;
		case 11: STI(cpu); break;
		case 12: JMP(cpu); break;
		case 13: err(cpu); break;
		case 14: LEA(cpu); break;
		case 15: TRAP(cpu); break;
		default:
			printf("Bad opcode: %d; quitting\n", (cpu->ir));
			cpu->running = 0;
	}
}
//Note: I am treating the bits in reverse order(0-15)as indices normally are in c than the bits in LC3 (15-0)
//to make it easier and avoid less confusion with selecting bits properly
int copyBits(int val, int left, int right){ //function to copy a selection of bits in a LC3 instruction code
	int m = right-left+1;
	int p = 15-right;
	int mask = ((1<<m)-1)<<p; //mask of 0s, m 1s, and p 0s
	int result = val & mask; //store the section of bits you are trying to copy
	result = result >> p; //right shift the result so your copied bits start at index 0
	return result;
}

void setCC(CPU *cpu, int val){ //set condition code
    if(val>0){
        cpu->cc=1;
    }
    if(val==0){
        cpu->cc = 0;
    }
    if(val<0){
        cpu->cc = -1;
    }
}
//implement condition code as its 3 bit value to compare against 3 bit branch mask
int getCC(CPU *cpu){
    if(cpu->cc==0)
        return 2; //010 CC value
    else if(cpu->cc>0)
        return 1; //001 CC value
    else
        return 4; //100 CC value
}

void BR(CPU *cpu){
    int pcOffset = copyBits(cpu->ir,7,15); // copy the last 9 bits in the PC instruction to get the PC offset
    int brMask = copyBits(cpu->ir,4,6);  //copy bits 11 to 9 to get the BRANCH Mask
    int compare = getCC(cpu);
    if ((compare & brMask)!=0){
        int oldPc = cpu ->pc;
        cpu -> pc += pcOffset;
        printf("BR number:%d Condition code:%d ; condition satisfied! New PC = %x + %x = %x\n",brMask,cpu->cc,oldPc,pcOffset,cpu->pc);
    }
    else{
        printf("BR number:%d Condition code:%d ; condition NOT satisify!\n",brMask,cpu->cc);
    }
    
}

void ADD(CPU *cpu){
	int checkBit = copyBits(cpu->ir,10,10); //check bit 5 to see if adding immediate or adding another reg
	int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
	int src1 = copyBits(cpu->ir,7,9); //src1
	if (checkBit==0){
		int src2 = copyBits(cpu->ir,13,15); //src2
		cpu -> reg[dst] = cpu->reg[src1]+cpu->reg[src2];
		printf("ADD R%d R%d 0 R%d ; reg[%d]=%x+%x=%x\n",dst,src1,src2,dst,cpu->reg[src1],
		cpu->reg[src2],cpu->reg[dst]);
	}
	else{
		int imm5 = copyBits(cpu->ir,11,15);
		cpu -> reg[dst] = cpu->reg[src1]+imm5;
		printf("ADD R%d R%d 1 %x ; reg[%d]=%x+%x=%x\n",dst,src1,imm5,dst,cpu->reg[src1],
		imm5,cpu->reg[dst]);
	}
    setCC(cpu,cpu->reg[dst]);
}

void LD(CPU *cpu){
    int pcOffset = copyBits(cpu->ir,7,15); // copy the last 9 bits in the PC instruction to get the PC offset
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    cpu ->reg[dst] = cpu ->mem[cpu->pc+pcOffset];
    printf("LD R%d %d ; reg[%x]<- M[%x] = %x\n",dst,pcOffset,dst,cpu->pc+pcOffset,cpu->mem[cpu->pc+pcOffset]);
    setCC(cpu,cpu->reg[dst]);
}

void ST(CPU *cpu){
    int src = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the src register
    int pcOffset = copyBits(cpu->ir,7,15); // copy the last 9 bits in the PC instruction to get the PC offset
    cpu->mem[cpu->pc+pcOffset] = cpu->reg[src];
    printf("ST R%d %x %x ; mem[%x] <-reg[%x] = %x,\n",src,cpu->pc,pcOffset,src,cpu->pc+pcOffset,cpu->reg[src]);
}

void JSR(CPU *cpu){
    int pcOffset = copyBits(cpu->ir,5,15); //copy the last 11 bits to get PCoffset11
    int bitToSignExtend = copyBits(cpu->ir,5,5); //copy leftmost bit in PCoffset11 to sign extend
    pcOffset = pcOffset>>(16-11); //pcOffset = 00000-PCoffset11 #
    if(bitToSignExtend==1){ //check if leftmost bit is 1, then sign extend 1 instead of 0:
        pcOffset = pcOffset|0xF400; //pcOffset = pcOffset|1111100000000000 -> 11111-PCoffset11 #
    }
    cpu -> reg[7] = cpu -> pc;
    cpu -> pc += pcOffset; // PC <- PC + SignExtend(PCOffset11)
    printf("JSR New pc = reg[%d] = %x\n",pcOffset,cpu->reg[pcOffset]);
}

void JSRR(CPU *cpu){
    int base = copyBits(cpu->ir,7,9); //copy bits 8 to 6 to get the Base in JSRR instruction
    int target = cpu ->reg[base];
    cpu -> reg[7] = cpu ->pc;
    cpu -> pc = target;
    printf("JSRR New pc = reg[%d] = %x\n",base,target);
}
void AND(CPU *cpu){
    int checkBit = copyBits(cpu->ir,10,10); //check bit 5 to see if & with immediate or & with another reg
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    int src1 = copyBits(cpu->ir,7,9); //src1
    if (checkBit==0){
        int src2 = copyBits(cpu->ir,13,15); //src2
        cpu -> reg[dst] = cpu->reg[src1] & cpu->reg[src2]; //AND R[dst], R[src1], R[src2]
        printf("AND R%d R%d 0 R%d ; reg[%d]=%x & %x=%x\n",dst,src1,src2,dst,cpu->reg[src1],
               cpu->reg[src2],cpu->reg[dst]);
    }
    else{
        int imm5 = copyBits(cpu->ir,11,15);
        cpu -> reg[dst] = cpu->reg[src1] & imm5; //AND R[dst], R[src1], imm5
        printf("AND R%d R%d 1 %x ; reg[%d]=%x & %x=%x\n",dst,src1,imm5,dst,cpu->reg[src1],imm5,cpu->reg[dst]);
    }
    setCC(cpu,cpu->reg[dst]);
}

void LDR(CPU *cpu){
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    int base = copyBits(cpu->ir,7,9); //copy bits 8 to 6 to get base
    int offset6 = copyBits(cpu->ir,10,15); //copy the rest of bits to get offset
    cpu->reg[dst] = cpu->mem[cpu->reg[base]+offset6]; //Destination reg <- M[base reg +offset]
    printf("LDR R%d R%x %x ; reg[%x] <-memory[reg[%x]+%x] = %x\n",dst,base,offset6,dst,base,offset6,cpu->reg[dst]);
    setCC(cpu,cpu->reg[dst]);
}

void STR(CPU *cpu){
    int src = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the source register
    int base = copyBits(cpu->ir,7,9); //copy bits 8 to 6 to get base
    int offset6 = copyBits(cpu->ir,10,15); //copy the rest of bits to get offset
    cpu -> mem[cpu->reg[base]+offset6] = cpu->reg[src]; // M[Base reg + offset]=source reg
    printf("STR R%d R%d %x ; memory[reg[%x]+%x] = reg[%x]= %x\n",src,base,offset6,base,offset6,src,cpu->reg[src]);
}

void RTI(CPU *cpu){
    printf("Error!");
}

void NOT(CPU *cpu){
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    int src = copyBits(cpu->ir,7,9); //src
    cpu->reg[dst]= ~cpu->reg[src]; //dst reg = NOT( src reg )
    printf("NOT R%d R%d ; reg[%x]<-~reg[%x] = %d \n",dst,src,dst,src,cpu->reg[dst]);
    setCC(cpu,cpu->reg[dst]);
}

void LDI(CPU *cpu){
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    int pcOffset = copyBits(cpu->ir,7,15); //copy the rest of bits to get PCoffset9
    cpu -> reg[dst] = cpu->mem[cpu->mem[cpu->pc+pcOffset]]; //Dst reg <- M[M[PC+offset]]
    printf("LDI R%d %x %x ; reg[%x] <- memory[memory[%x+%x]] = %x \n",dst,pcOffset,cpu->pc,dst,pcOffset,cpu->pc,cpu->reg[dst]);
    setCC(cpu,cpu->reg[dst]);
}

void STI(CPU *cpu){
    int src = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the source register
    int pcOffset = copyBits(cpu->ir,7,15); //copy the rest of bits to get PCoffset9
    cpu->mem[cpu->mem[cpu->pc+pcOffset]] = cpu->reg[src]; //M[M[PC+offset]] <- Source Register
    printf("STI R%d %x ; memory[memory[%x+%x]]<-reg[%x] = %x \n",src,pcOffset,cpu->pc,pcOffset,src,cpu->reg[src]);
}

void JMP(CPU *cpu){
    int base = copyBits(cpu->ir,7,9); //copy bits to get reg to jump to
    cpu->pc = cpu->reg[base];
    printf("JMP New pc = reg[%d] = %x\n",base,cpu->reg[base]);
}

void err(CPU *cpu){
    printf("Error!");
}

void LEA(CPU *cpu){
    int dst = copyBits(cpu->ir,4,6); // copy bits 11 to 9 to get the destination register
    int pcOffset = copyBits(cpu->ir,7,15); // copy the last 9 bits in the PC instruction to get the PC offset
    cpu -> reg[dst] = cpu->pc + pcOffset; //Dst reg <- PC + offset
    printf("LEA R%d %x %x ; Reg[%x] <- %x + %x = %x \n",dst,cpu->pc,pcOffset,dst,cpu->pc,pcOffset,cpu->reg[dst]);
    setCC(cpu,cpu->reg[dst]);
}

void TRAP(CPU *cpu){
    int trapVec = copyBits(cpu->ir,8,15); //copy last 8 bits of instruction to get the trap vector
    char ch;
    int pt;
    switch (trapVec) {
        case 32: //x20 (hex) - GETC
            ch = getc(stdin);
            cpu->reg[0] = cpu->reg[0]&0; //R0 = 0
            cpu->reg[0] = cpu->reg[0]|ch; //R0[7..0]=ch and R0[15..8]=0
            printf("New Reg value: R0: %x \n",cpu->reg[0]);
            break;
        case 33: //x21 - OUT
            ch = copyBits(cpu->reg[0],8,15); //copy bits 8-15 in R0
            printf("%c",ch);
            break;
        case 34: //x22 - PUTS
            pt = cpu->reg[0];
            while(cpu->mem[pt]){
                printf("%c",cpu->mem[pt]);
                pt++;
            }
            break;
        case 35: //x23 - IN
            printf("input a char: ");
            ch = getc(stdin);
            cpu->reg[0] = cpu->reg[0]&0; //R0 = 0
            cpu->reg[0] = cpu->reg[0]|ch; //R0[7..0]=ch and R0[15..8]=0
            printf("New Reg value: R0: %x \n",cpu->reg[0]);
            break;
        case 36: //x24
            printf("Error, execution will be halted\n");
            cpu->running=0;
            break;
        case 37: //x25 - HALT
            cpu->running = 0;
            break;
    }
}