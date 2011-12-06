#include <stdio.h>
#include <sys/sysinfo.h>

#define LOAD_PERCENT_CONVERSION (float)(1 << SI_LOAD_SHIFT)
#define ln_br putchar('\n')

int main(){
    // Defining blank sysinfo struct.
    struct sysinfo info;
    sysinfo(&info);
    // Load up sysinfo
    // for struct info, type `man sysinfo` into the shell.
    
    printf("%.02f%% System Load - Past Min", (info.loads[0] / LOAD_PERCENT_CONVERSION));
    ln_br;
    printf("%d processes.", info.procs);
    ln_br;
    
    // We're good!
    return 0;
}