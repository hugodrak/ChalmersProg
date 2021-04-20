/*
 * 	startup.c
 *
 */
__attribute__((naked)) __attribute__((section (".start_section")) )
void startup ( void )
{
__asm__ volatile(" LDR R0,=0x2001C000\n");		/* set stack */
__asm__ volatile(" MOV SP,R0\n");
__asm__ volatile(" BL main\n");					/* call main */
__asm__ volatile(".L1: B .L1\n");				/* never return */
}

#define GPIO_D 0x40020c00
#define GPIO_E 0x40021000

#define GPIO_MODER 0
#define GPIO_IDR 0x10
#define GPIO_ODR 0x14

#define GPIO_D_MODER ((volatile unsigned long*) (GPIO_D+GPIO_MODER))
#define GPIO_D_IDR ((volatile unsigned short*)(GPIO_D+GPIO_IDR))
#define GPIO_D_ODR ((volatile unsigned short*)(GPIO_D+GPIO_ODR))


#define GPIO_E_MODER ((volatile unsigned long*) (GPIO_E+GPIO_MODER))
#define GPIO_E_IDR ((volatile unsigned short*)(GPIO_E+GPIO_IDR))
#define GPIO_E_ODR ((volatile unsigned short*)(GPIO_E+GPIO_ODR))

unsigned char keycodes[] = {1,2,3,'a',4,5,6,'b',7,8,9,'c','f',0,'e','d'};

void app_init(void){
	*GPIO_D_MODER=0x00005555;
	*GPIO_E_MODER=0x00005500;
	//*((unsigned long*)(GPIO_D+GPIO_MODER) =
}

unsigned char readKey(){
	
	for(unsigned char row_index=0; row_index<4;row_index++){
		
		unsigned short row_mask = 0x10<<row_index;
		*GPIO_E_ODR = row_mask;
		
		unsigned short data = *GPIO_E_IDR;
		
		for(unsigned char column_index=0;column_index<4;column_index++){
			unsigned short column_mask=1<<column_index;
			
			if((data&column_mask)!=0){
				return row_index*4+column_index;
			}
	
		}
	}
	
	return 0xff;
	
	
}


void main(void)
{
	unsigned char c;
	app_init();
	while(1){
		c=readKey();//(unsigned char) *GPIO_E_IDR;//((unsigned short *) 0x40021010);
		*GPIO_D_ODR=c;
	}
	
}

