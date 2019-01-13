/** Program to load a PRU program that flashes an LED until a button is
*   pressed. By Derek Molloy, for the book Exploring BeagleBone
*   based on the example code at:
*   http://processors.wiki.ti.com/index.php/PRU_Linux_Application_Loader_API_Guide
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <prussdrv.h>
#include <pruss_intc_mapping.h>

#define PRU_NUM	0   // using PRU0 for these examples
#define MMAP_LOC "/sys/class/uio/uio0/maps/map1/"

unsigned int readFileValue(char filename[]){
   FILE* fp;
   unsigned int value = 0;
   fp = fopen(filename, "rt");
   fscanf(fp, "%x", &value);
   fclose(fp);
   return value;
}

int main (int argc, char *argv[])
{
  for(int i=0; i<argc; i++){
    printf("Arg %i %s\n", i, argv[i]);
  }
  printf("yay %i", argc);
  tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;

  if(getuid() != 0) {
    printf("You must run this program as root. Exiting.\n");
    exit(EXIT_FAILURE);
  }

  if( argc == 1 ) {
    printf("USAGE\n");
    exit(EXIT_FAILURE);
  }
 
  prussdrv_init();

  if( strcmp(argv[1], "load") == 0 ) {
    if(argc != 3){
      printf("Fail1");
      exit(EXIT_FAILURE);
    }
    prussdrv_exec_program (PRU_NUM, argv[2]);
  } 
  else if ( strcmp(argv[1], "stop") == 0) {
    prussdrv_pru_disable(PRU_NUM);
  }

  prussdrv_exit();
  return EXIT_SUCCESS;
}
