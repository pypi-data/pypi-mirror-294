//Autogenerated PPP header from /panda/panda/plugins/osi/os_intro.h

typedef void (*on_get_processes_t)(CPUState *, GArray **);
void ppp_add_cb_on_get_processes(on_get_processes_t);
bool ppp_remove_cb_on_get_processes(on_get_processes_t);
typedef void (*on_get_process_handles_t)(CPUState *, GArray **);
void ppp_add_cb_on_get_process_handles(on_get_process_handles_t);
bool ppp_remove_cb_on_get_process_handles(on_get_process_handles_t);
typedef void (*on_get_current_process_t)(CPUState *, OsiProc **);
void ppp_add_cb_on_get_current_process(on_get_current_process_t);
bool ppp_remove_cb_on_get_current_process(on_get_current_process_t);
typedef void (*on_get_current_process_handle_t)(CPUState *, OsiProcHandle **);
void ppp_add_cb_on_get_current_process_handle(on_get_current_process_handle_t);
bool ppp_remove_cb_on_get_current_process_handle(on_get_current_process_handle_t);
typedef void (*on_get_process_t)(CPUState *, const OsiProcHandle *, OsiProc **);
void ppp_add_cb_on_get_process(on_get_process_t);
bool ppp_remove_cb_on_get_process(on_get_process_t);
typedef void (*on_get_proc_mem_t)(CPUState *cpu, const OsiProc *p, OsiProcMem **);
void ppp_add_cb_on_get_proc_mem(on_get_proc_mem_t);
bool ppp_remove_cb_on_get_proc_mem(on_get_proc_mem_t);
typedef void (*on_get_modules_t)(CPUState *, GArray **);
void ppp_add_cb_on_get_modules(on_get_modules_t);
bool ppp_remove_cb_on_get_modules(on_get_modules_t);
typedef void (*on_get_mappings_t)(CPUState *, OsiProc *, GArray**);
void ppp_add_cb_on_get_mappings(on_get_mappings_t);
bool ppp_remove_cb_on_get_mappings(on_get_mappings_t);
typedef void (*on_get_file_mappings_t)(CPUState *, OsiProc *, GArray**);
void ppp_add_cb_on_get_file_mappings(on_get_file_mappings_t);
bool ppp_remove_cb_on_get_file_mappings(on_get_file_mappings_t);
typedef void (*on_get_heap_mappings_t)(CPUState *, OsiProc *, GArray**);
void ppp_add_cb_on_get_heap_mappings(on_get_heap_mappings_t);
bool ppp_remove_cb_on_get_heap_mappings(on_get_heap_mappings_t);
typedef void (*on_get_stack_mappings_t)(CPUState *, OsiProc *, GArray**);
void ppp_add_cb_on_get_stack_mappings(on_get_stack_mappings_t);
bool ppp_remove_cb_on_get_stack_mappings(on_get_stack_mappings_t);
typedef void (*on_get_unknown_mappings_t)(CPUState *, OsiProc *, GArray**);
void ppp_add_cb_on_get_unknown_mappings(on_get_unknown_mappings_t);
bool ppp_remove_cb_on_get_unknown_mappings(on_get_unknown_mappings_t);
typedef void (*on_get_mapping_by_addr_t)(CPUState *, OsiProc *, const target_ptr_t, OsiModule **);
void ppp_add_cb_on_get_mapping_by_addr(on_get_mapping_by_addr_t);
bool ppp_remove_cb_on_get_mapping_by_addr(on_get_mapping_by_addr_t);
typedef void (*on_get_mapping_base_address_by_name_t)(CPUState *, OsiProc *, const char *, target_ptr_t *);
void ppp_add_cb_on_get_mapping_base_address_by_name(on_get_mapping_base_address_by_name_t);
bool ppp_remove_cb_on_get_mapping_base_address_by_name(on_get_mapping_base_address_by_name_t);
typedef void (*on_has_mapping_prefix_t)(CPUState *, OsiProc *, const char *, bool *);
void ppp_add_cb_on_has_mapping_prefix(on_has_mapping_prefix_t);
bool ppp_remove_cb_on_has_mapping_prefix(on_has_mapping_prefix_t);
typedef void (*on_get_current_thread_t)(CPUState *, OsiThread **);
void ppp_add_cb_on_get_current_thread(on_get_current_thread_t);
bool ppp_remove_cb_on_get_current_thread(on_get_current_thread_t);

typedef void (*on_get_process_pid_t)(CPUState *, const OsiProcHandle *, target_pid_t *);
void ppp_add_cb_on_get_process_pid(on_get_process_pid_t);
bool ppp_remove_cb_on_get_process_pid(on_get_process_pid_t);
typedef void (*on_get_process_ppid_t)(CPUState *, const OsiProcHandle *, target_pid_t *);
void ppp_add_cb_on_get_process_ppid(on_get_process_ppid_t);
bool ppp_remove_cb_on_get_process_ppid(on_get_process_ppid_t);

typedef void (*on_task_change_t)(CPUState *);
void ppp_add_cb_on_task_change(on_task_change_t);
bool ppp_remove_cb_on_task_change(on_task_change_t);

