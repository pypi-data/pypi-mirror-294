//Autogenerated PPP header from /panda/panda/plugins/callwitharg/callwitharg_ppp.h

typedef void (*on_call_match_num_t)(CPUState *env, target_ulong func_addr, target_ulong *args, uint32_t matching_idx, uint32_t args_read);
void ppp_add_cb_on_call_match_num(on_call_match_num_t);
bool ppp_remove_cb_on_call_match_num(on_call_match_num_t);
typedef void (*on_call_match_str_t)(CPUState *env, target_ulong func_addr, target_ulong *args, char* value, uint32_t matching_idx, uint32_t args_read);
void ppp_add_cb_on_call_match_str(on_call_match_str_t);
bool ppp_remove_cb_on_call_match_str(on_call_match_str_t);

