void secure_init(void);
char *secure_malloc(unsigned int);
void secure_free(char*);
void __heap_chk_fail(char*);
void __abort(char*);
