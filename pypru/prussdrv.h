typedef void *(*prussdrv_function_handler) (void *);

typedef struct __sysevt_to_channel_map {
    short sysevt;
    short channel;
} tsysevt_to_channel_map;

typedef struct __channel_to_host_map {
    short channel;
    short host;
} tchannel_to_host_map;

typedef struct __pruss_intc_initdata {
    // Enabled SYSEVTs - Range:0..63
    // {-1} indicates end of list
    char sysevts_enabled[64];
    // SysEvt to Channel map. SYSEVTs - Range:0..63 Channels -Range: 0..9
    // {-1, -1} indicates end of list
    tsysevt_to_channel_map sysevt_to_channel_map[64];
    // Channel to Host map.Channels -Range: 0..9  HOSTs - Range:0..9
    // {-1, -1} indicates end of list
    tchannel_to_host_map channel_to_host_map[10];
    // 10-bit mask - Enable Host0-Host9 {Host0/1:PRU0/1, Host2..9 : PRUEVT_OUT0..7)
    unsigned int host_enable_bitmask;
} tpruss_intc_initdata;

int prussdrv_init(void);

int prussdrv_open(unsigned int pru_evtout_num);

int prussdrv_pru_reset(unsigned int prunum);

int prussdrv_pru_disable(unsigned int prunum);

int prussdrv_pru_enable(unsigned int prunum);

int prussdrv_pru_write_memory(unsigned int pru_ram_id, unsigned int wordoffset, unsigned int *memarea, unsigned int bytelength);

int prussdrv_pruintc_init(tpruss_intc_initdata * prussintc_init_data);

int prussdrv_map_l3mem(void **address);

int prussdrv_map_extmem(void **address);

int prussdrv_map_prumem(unsigned int pru_ram_id, void **address);

int prussdrv_map_peripheral_io(unsigned int per_id, void **address);

unsigned int prussdrv_get_phys_addr(void *address);

void *prussdrv_get_virt_addr(unsigned int phyaddr);

int prussdrv_pru_wait_event(unsigned int pru_evtout_num);

int prussdrv_pru_send_event(unsigned int eventnum);

int prussdrv_pru_clear_event(unsigned int eventnum);

int prussdrv_pru_send_wait_clear_event(unsigned int send_eventnum, unsigned int pru_evtout_num, unsigned int ack_eventnum);

int prussdrv_exit(void);

int prussdrv_exec_program(int prunum, char *filename);

int prussdrv_start_irqthread(unsigned int pru_evtout_num, int priority, prussdrv_function_handler irqhandler);

tpruss_intc_initdata * pruss_intc_initdata_ptr;
