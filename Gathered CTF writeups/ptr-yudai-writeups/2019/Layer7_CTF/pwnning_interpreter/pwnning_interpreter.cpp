#include <cstring>
#include <cstdio>
#include <iostream>
#include <csignal>
#include <cstdlib>

#define PTR 0x1400
#define CHR 0x1491
#define INTEGER 0x14ac
#define NONE 0x18ab

#define IS_OPER(POS) (*POS == '+' || *POS == '-' || *POS == '/' || *POS == '%' || *POS == '*' || *POS == '[' || *POS == '=')

using namespace std;

void time_out(int signum) {
	std::cout << "Time out!!" << std::endl;
	exit(-1);
}

void set() {
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    signal(SIGALRM, time_out);
    __asm__("mov $0x3c, %rdi");
    __asm__("mov $0x25, %rax");
    __asm__("syscall");
}

void mystrcpy(char *src, char *dst, size_t size) {
	for(int i = 0; i < size; ++i) {
		src[i] = dst[i];
	}
	src[size] = '\0';
}

void check_space();
bool interprete(char *);
char* string_proc(char *, size_t);
__int64_t arithmetic(__int64_t);

class variable {
public:
	__int64_t value[16];
	short type;
	char *name;
	short size;
	bool is_ref;
	bool is_arr;
	variable *next;

	variable() {
		memset(this->value, '\0', 0x80);
		this->type = NONE;
		this->name = (char*)malloc(0x400);
		strcpy(this->name, "HEAD");
		this->size = 0;
		this->is_ref = false;
		this->next = NULL;
		this->is_arr = false;
	}

	variable(char* name, char* value, size_t size, bool is_arr) {
		if(strlen(value) != 0) 
			memcpy(this->value, value, size);
		this->type = CHR;
		this->name = name;
		this->size = size;
		this->is_ref = false;
		this->next = NULL;
		this->is_arr = is_arr;
	}

	variable(char* name, __int64_t value, size_t size, bool is_arr) {
		this->value[0] = value;
		this->type = INTEGER;
		this->name = name;
		this->size = size;
		this->is_ref = false;
		this->next = NULL;
		this->is_arr = is_arr;	
	}

	variable(char*name, variable* value, size_t size) {
		this->value[0] = (__int64_t	)value;
		this->type = PTR;
		this->name = name;
		this->size = size;
		this->is_ref = false;
		this->next = NULL;
		this->is_arr = false;
	}

	void assignment(short type, char *value, size_t index, size_t size) {
		this->type = type;
		mystrcpy(&((char*)this->value)[index], value, size);
		this->size = size;
	}
	
	void assignment(short type, __int64_t value, size_t index, size_t size) {
		this->type = type;
		this->value[index] = value;
		this->size = size;
	}

	void assignment(short type, variable* value) {
		this->type = type;
		this->value[0] = (__int64_t)value;
		this->size = 1;
	}

	~variable() {
		std::cout << '\'' << this->name << '\'' << " has been erased" << std::endl;
		memset(this->name, '\0', strlen(this->name));
		delete this->name;
	}

};

namespace iostream {
	void read(char *buf, size_t size) {
		int len;
		int i;
		for (i = 0; i < size; ++i) {
		    __asm__("xor %rdi, %rdi");
		    __asm__ __volatile__(
		    	"inc %%rax\n\t" 
		    	: : "r" (buf + i) : "memory"
		    );
		    __asm__("dec %rax");
		    __asm__("mov %rax, %rsi");
		    __asm__("mov $1, %rdx");
		    __asm__("mov $0, %rax");
		    __asm__("syscall");
		    __asm__ __volatile__(
		    	"nop\n\t"
		    	: "=r" (len) : : "memory");
		    if(buf[i] == '\n') {
		    	buf[i] = '\0';
		    	break;
		    }
		}
	}

	void write(char *buf, size_t size) {
	    __asm__("mov $1, %rdi");
	    __asm__ __volatile__(
	    	"inc %%rdx\n\t" 
	    	: : "r" (size) : "memory"
	    );
	    __asm__("mov %rax, %rdx");
	    __asm__ __volatile__(
	    	"inc %%rax\n\t" 
	    	: : "r" (buf) : "memory"
	    );
	    __asm__("dec %rax");
	    __asm__("mov %rax, %rsi");
	    __asm__("mov $1, %rax");
	    __asm__("syscall");
	}
}

namespace T {
	string Exit = "exit";
	string Int = "int";
	string Chr = "char";
	string Pointer = "ptr";
	string Ref = "*";
	string Del = "del";
}

char *Go = ">>";
char *POS;
char PROGRAM[0x400];
variable DUM;
variable *HEAD = &DUM;

int main() {
	set();
	std::cout << "=======================================" << std::endl;
	std::cout << "=       -----------------------       =" << std::endl;
	std::cout << "=       |       V 0.0.1       |       =" << std::endl;
	std::cout << "=       | pwnning interpreter |       =" << std::endl;
	std::cout << "=       -----------------------       =" << std::endl;
	std::cout << "=          Can you exploit ??         =" << std::endl;
	std::cout << "=        I Think it is so safe        =" << std::endl;
	std::cout << "=                                     =" << std::endl;
	std::cout << "=    ex 1) int a = 1234 + 123413;     =" << std::endl;
	std::cout << "=    ex 2) char a[128] = \"12345\";     =" << std::endl;
	std::cout << "=    ex 3) ptr a=&a;int b;char c;     =" << std::endl;
	std::cout << "=                                     =" << std::endl;
	std::cout << "=======================================" << std::endl;
	int saved_sp;
	do{
		memset(PROGRAM, '\0', 0x400);
		std::cout << Go;
		iostream::read(PROGRAM, 0x400);
	} while (interprete(PROGRAM));
	exit(0);
}

void check_space(){
	while (true) {
		if(*POS == ' ') POS += 1;
		else break;
	}
}

bool interprete(char* program) {
	char *data_type = NULL;
	char check_ref[8] = {'\0', };
	size_t type_len;
	POS = program;
	check_ref[0] = program[0];
	data_type = strchr(program, ' ');

	if(data_type != NULL){
		type_len = data_type - program;
		data_type = new char[0x200];
		memcpy(data_type, program, type_len); 
	}

	if(*program == '\0') return true;

	if(T::Exit.compare(program) == 0) {
		std::cout << "Thank you for using~" << std::endl;
		return false;
	}

	else if (check_ref[0] == '"') { 
		POS += 1;
		char *local_str = NULL;
		local_str = strchr(POS, '"');
		
		if(local_str == NULL) { 
			std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
			return false;
		}

		size_t len; 
		len = local_str - POS;
		local_str = new char[len];
		memcpy((void *)local_str, (const void *)POS, len);
		POS += len + 1;
		check_space(); 

		local_str = string_proc(local_str, len);
		
		std::cout << '"' << local_str << '"' << std::endl;
		memset(local_str, '\0', strlen(local_str));
		delete local_str;
	}

	else if ((check_ref[0] <= '9' && check_ref[0] >= '0') || (check_ref[0] == '-' || check_ref[0] == '+')) {
		__int64_t value = atol(POS);
		__int64_t result = 0;
		if(check_ref[0] == '+' || check_ref[0] == '-') POS += 1;

		for(POS;;++POS) {
			if(*POS > '9' || *POS < '0') break;
		}
		check_space();

		result = arithmetic(value);
		std::cout << '"' << result << '"' << std::endl;
	}

	else if(T::Ref.compare(check_ref) == 0) {	
		size_t ref_cnt = 0;
		char *var_name;
		size_t name_len;
		char *save_pos;
		variable* node = HEAD;
		__int64_t result = 0;

		for(POS;;++POS) {
			if(*POS == '*') ++ref_cnt;
			else if(*POS == ' ');
			else if(*POS == '&') --ref_cnt;
			else break;
		}

		if(ref_cnt < 0) {
			std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
			return false;
		}
		save_pos = POS;

		for(POS;;++POS) {
			if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
		}

		name_len = POS - save_pos;
		var_name = new char[name_len];
		memcpy(var_name, save_pos, name_len);
		while(node->next) {
			node = node->next;
			if(strcmp(node->name, var_name) == 0) break;
		}

		if(strcmp(node->name, var_name) != 0) {
			std::cout << "ERROR: unexpected token..." << std::endl;
			return false;
		}

		for(int i = 0;i < ref_cnt; ++i) {
			if(node->type != PTR) {
				std::cout << "You can't reference anything except pointer...!!" << std::endl;
				return false;
			}
			
			else if ((variable*)node->value[0] == NULL) {
				std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
				return false;
			}

			if(node->is_ref == true) {
				std::cout << "You can reference ptr just one time...!" << std::endl;
				return false;
			}
			
			node->is_ref = true;
			node = (variable*)(node->value[0]);
		}
		memset(var_name, '\0', name_len);
		delete var_name;
		check_space();
		
		if(*POS == '=') {
			save_pos = POS;
			char *save;
			char *name;
			size_t n_len;
			variable *find = HEAD;
			*POS = '+';
			++POS;
			check_space();
			
			if((*POS <= '9' && *POS >= '0') || (*POS == '+' || *POS == '-')) {
				size_t assignment_size = node->size;
				if(node->type == CHR) assignment_size /= 8;
				POS = save_pos;
				node->assignment(INTEGER, arithmetic(0), 0, assignment_size);
			}

			else if (*POS == '"') {
				POS = save_pos;
				char *result = string_proc((char*)malloc(0x400), 0);
				size_t assignment_size = node->size;
				if(node->type != CHR) assignment_size *= 8;
				node->assignment(CHR, result, 0, assignment_size);
				memset(result, '\0', strlen(result));
				delete result;
			}

			else if (*POS == '*') {
				ref_cnt = 0;
				for(POS;;++POS) {
					if(*POS == '*') ++ref_cnt;
					else if(*POS == ' ');
					else if(*POS == '&') --ref_cnt;
					else break;
				}
				save = POS;
				for(POS;;++POS) {
					if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
				}
				n_len = POS - save;
				name = new char[n_len];
				memcpy(name, save, n_len);
				check_space();
				while(find->next) {
					find = find->next;
					if(strcmp(find->name, name) == 0) break;
				}

				if(strcmp(find->name, name) != 0) {
					std::cout << "ERROR: unexpected token..." << std::endl;
					return false;
				}

				memset(name, '\0', n_len);
				delete name;

				for(int i = 0;i < ref_cnt; ++i) {
					if(find->type != PTR) {
						std::cout << "You can't reference anything except pointer...!!" << std::endl;
						return false;
					}
					else if ((variable*)find->value[0] == NULL) {
						std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
						return false;
					}
					if(find->is_ref == true) {
						std::cout << "You can reference ptr just one time...!" << std::endl;
						return false;
					}
					find->is_ref = true;
					find = (variable*)(find->value[0]);
				}

				if(find->type == INTEGER) {
					POS = save_pos;	
					node->assignment(INTEGER, arithmetic(0), 0, find->size);
				}
				else if (find->type == CHR) {
					POS = save_pos;
					char *result = string_proc((char*)malloc(0x400), 0);
					node->assignment(CHR, result, 0, find->size);
					memset(result, '\0', strlen(result));
					delete result;
				}
				else if(find->type == PTR) {
					node->assignment(PTR, (variable*)find->value[0]);
				}
			}

			else if (*POS == '&') {
				char *name;
				size_t n_len;
				variable *find = HEAD;
				++POS;
				check_space();
				save = POS;
				for(POS;;++POS) {
					if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
				}
				n_len = POS - save;
				name = new char[n_len];
				memcpy(name, save_pos, n_len);
				while(find->next) {
					find = find->next;
					if(strcmp(find->name, name) == 0) break;
				}
				
				if(strcmp(find->name, name) != 0) {
					std::cout << "ERROR: unexpected token..." << std::endl;
					return false;
				}

				node->assignment(PTR, find);
				memset(name, '\0', n_len);
				delete name;
			}
		}
		
		else if (IS_OPER(POS)) {
			if(*POS == '[') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}
			if(node->type == CHR) {
				if(*POS != '+') {
					std::cout << "You can't do anything except \"add\"" << std::endl;
					return false;
				}

				char *result;
				result = new char[node->size];
				mystrcpy(result, (char*)node->value, strlen((char*)node->value));
				result = string_proc(result, node->size);
				std::cout << '"' << result << '"' << std::endl;
				memset(result, '\0', strlen(result));
				delete result;
			}
			
			else if(node->type == INTEGER) {
				if(*POS == '[') {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}
				std::cout << '"' << arithmetic(node->value[0]) << '"' << std::endl;
			}

			else if(node->type == PTR) {
				std::cout << "ERROR: Pointer cannot be operated.." << std::endl;
				return false;
			}
		}
		
		else if(*POS == ';') {
			if(node->type == INTEGER) {
				std::cout << '"' << node->value[0] << '"' << std::endl;
			}
			
			else if(node->type == CHR) {
				std::cout << '"';
				iostream::write((char*)node->value, node->size);
				std::cout << '"' << std::endl;
			}

			else {
				std::cout << "ERROR: Unexpected variable type..." << std::endl;
				return false;
			}
		}
	}

	else if(check_ref[0] == ';');
	
	else if(check_ref[0] == ' ') {
		check_space();
		--POS;
	}

	else if(data_type != NULL) {
		if(T::Int.compare(data_type) == 0) {
			char *var_name;
			size_t name_len;
			char *save_pos;
			size_t arr_size = 1;
			bool is_arr = false;
			variable* node = HEAD;
			variable* new_var = NULL;
			__int64_t result = 0;

			POS += 3;
			check_space();
			save_pos = POS;
			if(*POS <= '9' && *POS >= '0') {
				std::cout << "Error: Unexpected number..!" << std::endl;
				return false;
			}
			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}
			if(*POS != '=' && *POS != ' ' && *POS != ';' && *POS != '[') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			check_space();
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) {
					std::cout << '\'' << var_name << '\'' << " has already been declared..!" << std::endl;
					return false;
				}
			}
			
			if(*POS == '=') *POS = '+';

			else if(*POS == '[') {
				is_arr = true;
				POS += 1;
				save_pos = POS;
				for(int i = 0; i < 4; ++i) {
					if(*POS == ']') break;
					else if(*POS > '9' || *POS <'0') {
						std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
						return false;
					}
					++POS;
				}

				if(*POS != ']') {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}
				POS++;
				check_space();
				arr_size = atol(save_pos);
				if(arr_size < 1 || arr_size > 0x10) {
					std::cout << "ERROR: Array Size Error!!" << std::endl;
					return false;
				}
				if(*POS == '=') *POS = '+';
			}

			result = arithmetic(0);
			new_var = new variable(var_name, result, arr_size, is_arr);
			node->next = new_var;
		}

		else if(T::Chr.compare(data_type) == 0) {
			char *var_name;
			size_t name_len;
			char *save_pos;
			size_t arr_size = 1;
			bool is_arr = false;
			variable* node = HEAD;
			variable* new_var = NULL;
			char* result = NULL;

			POS += 4;
			check_space();
			save_pos = POS;

			if(*POS <= '9' && *POS >= '0') {
				std::cout << "Error: Unexpected number..!" << std::endl;
				return false;
			}

			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			if(*POS != '=' && *POS != ' ' && *POS != ';' && *POS != '[') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			check_space();
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) {
					std::cout << '\'' << var_name << '\'' << " has already been declared..!" << std::endl;
					return false;
				}
			}
			
			if(*POS == '=') *POS = '+';

			else if(*POS == '[') {
				is_arr = true;
				POS += 1;
				save_pos = POS;
				for(int i = 0; i < 4; ++i) {
					if(*POS == ']') break;
					else if(*POS > '9' || *POS <'0') {
						std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
						return false;
					}
					++POS;
				}

				if(*POS != ']') {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}
				POS++;
				check_space();
				arr_size = atol(save_pos);
				if(arr_size < 1 || arr_size > 0x80) {
					std::cout << "ERROR: Array Size Error!!" << std::endl;
					return false;
				}
				if(*POS == '=') *POS = '+';
			}

			result = string_proc((char*)malloc(0x400), 0);
			if(strlen(result) > arr_size) {
				std::cout << "Out Of Boundary check!" << std::endl;
				return false;
			}
			new_var = new variable(var_name, result, arr_size, is_arr);
			node->next = new_var;

			memset(result, '\0', strlen(result));
			delete result;
		}

		else if(T::Pointer.compare(data_type) == 0) {
			char *var_name;
			size_t name_len;
			char *save_pos;
			variable* node = HEAD;
			variable* new_var = NULL;
			variable* result = NULL;

			POS += 3;
			check_space();
			save_pos = POS;
			if(*POS <= '9' && *POS >= '0') {
				std::cout << "Error: Unexpected number..!" << std::endl;
				return false;
			}

			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			if(*POS != '=' && *POS != ' ' && *POS != ';' && *POS != '[') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			check_space();
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) {
					std::cout << '\'' << var_name << '\'' << " has already been declared..!" << std::endl;
					return false;
				}
			}

			if(*POS == '=') {
				char *dst_var;
				size_t dst_len;
				size_t ref_cnt = 0;
				variable *dst = HEAD;
				bool is_ptr = true;
				POS += 1;
				check_space();

				if(*POS == '&') {
					is_ptr = false;
					POS += 1;
					check_space();
				}

				else if (*POS == '*') {
					for(POS;;++POS) {
						if(*POS == '*') ++ref_cnt;
						else if(*POS == ' ');
						else if(*POS == '&') --ref_cnt;
						else break;
					}
				}

				if(ref_cnt < 0) {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}

				save_pos = POS;
				 
				for(POS;;++POS) {
					if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
				}

				dst_len = POS - save_pos;
				dst_var = new char[dst_len];
				memcpy(dst_var, save_pos, dst_len);
				
				while(dst->next) {
					dst = dst->next;
					if(strcmp(dst->name, dst_var) == 0) break;
				}

				if(strcmp(dst->name, dst_var) != 0) {
					std::cout << "ERROR: unexpected token..." << std::endl;
					return false;
				}

				for(int i = 0;i < ref_cnt; ++i) {
					if(dst->type != PTR) {
						std::cout << "You can't reference anything except pointer...!!" << std::endl;
						return false;
					}
					else if ((variable*)node->value[0] == NULL) {
						std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
						return false;
					}
					if(dst->is_ref == true) {
						std::cout << "You can reference ptr just one time...!" << std::endl;
						return false;
					}
					dst->is_ref = true;
					dst = (variable*)(dst->value[0]);
				}
				
				if(is_ptr) result = (variable*)(dst->value[0]);
				else result = dst;
				check_space();
				memset(dst_var, '\0', dst_len);
				delete dst_var;
			}

			else if(*POS == '[') {
				std::cout << "ERROR: I Don't support pointer array!" << std::endl;
				return false;
			}

			else if(*POS != ';') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}

			new_var = new variable(var_name, result, 1);
			node->next = new_var;
		}

		else if(T::Del.compare(data_type) == 0) {
			if(HEAD->next == NULL) {
				std::cout << "ERROR: Variable list is empty..!" << std::endl;
				return false;
			}
			POS += 3;
			char *save_pos;
			variable *node = HEAD;
			variable *del = NULL;
			char *var_name;
			size_t name_len;
			check_space();
			save_pos = POS;
			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			check_space();
			if(*POS != ';') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}
			while(node->next->next) {
				if(strcmp(node->next->name, var_name) == 0) break;
				node = node->next;
			}

			if(strcmp(node->next->name, var_name) != 0) {
				std::cout << "ERROR: unexpected token..." << std::endl;
				return false;
			}
			del = node->next;
			node->next = del->next;
			memset(del->value, '\0', 0x80);
			delete del;
		}
		
		else {
			char *var_name;
			size_t name_len;
			char *save_pos;
			variable* node = HEAD;
			__int64_t result = 0;

			save_pos = POS;

			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) break;
			}

			if(strcmp(node->name, var_name) != 0) {
				std::cout << "ERROR: unexpected token..." << std::endl;
				return false;
			}

			check_space();
			memset(var_name, '\0', name_len);
			delete var_name;
			
			if(*POS == '=') {
				save_pos = POS;
				char *save;
				char *name;
				size_t n_len;
				size_t ref_cnt = 0;
				variable *find = HEAD;
				*POS = '+';
				++POS;
				check_space();
				
				if((*POS <= '9' && *POS >= '0') || (*POS == '+' || *POS == '-')) {
					size_t assignment_size = node->size;
					if(node->type == CHR) assignment_size /= 8;
					POS = save_pos;
					node->assignment(INTEGER, arithmetic(0), 0, assignment_size);
				}

				else if (*POS == '"') {
					POS = save_pos;
					char *result = string_proc((char*)malloc(0x400), 0);
					size_t assignment_size = node->size;
					if(node->type != CHR) assignment_size *= 8;
					node->assignment(CHR, result, 0, assignment_size);
					memset(result, '\0', strlen(result));
					delete result;
				}

				else if (*POS == '*') {
					for(POS;;++POS) {
						if(*POS == '*') ++ref_cnt;
						else if(*POS == ' ');
						else if(*POS == '&') --ref_cnt;
						else break;
					}
					save = POS;
					for(POS;;++POS) {
						if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
					}
					n_len = POS - save;
					name = new char[n_len];
					memcpy(name, save, n_len);
					check_space();
					while(find->next) {
						find = find->next;
						if(strcmp(find->name, name) == 0) break;
					}

					if(strcmp(find->name, name) != 0) {
						std::cout << "ERROR: unexpected token..." << std::endl;
						return false;
					}

					memset(name, '\0', n_len);
					delete name;

					for(int i = 0;i < ref_cnt; ++i) {
						if(find->type != PTR) {
							std::cout << "You can't reference anything except pointer...!!" << std::endl;
							return false;
						}
						else if ((variable*)find->value[0] == NULL) {
							std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
							return false;
						}
						if(find->is_ref == true) {
							std::cout << "You can reference ptr just one time...!" << std::endl;
							return false;
						}
						find->is_ref = true;
						find = (variable*)(find->value[0]);
					}

					if(find->type == INTEGER) {
						POS = save_pos;	
						node->assignment(INTEGER, arithmetic(0), 0, find->size);
					}
					else if (find->type == CHR) {
						POS = save_pos;
						char *result = string_proc((char*)malloc(0x400), 0);
						node->assignment(CHR, result, 0, find->size);
						memset(result, '\0', strlen(result));
						delete result;
					}
					else if(find->type == PTR) {
						node->assignment(PTR, (variable*)find->value[0]);
					}
				}

				else if (*POS == '&') {
					char *name;
					size_t n_len;
					variable *find = HEAD;
					++POS;
					check_space();
					save = POS;

					for(POS;;++POS) {
						if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
					}
					
					n_len = POS - save;
					name = new char[n_len];
					memcpy(name, save_pos, n_len);
					
					while(find->next) {
						find = find->next;
						if(strcmp(find->name, name) == 0) break;
					}
					
					if(strcmp(find->name, name) != 0) {
						std::cout << "ERROR: unexpected token..." << std::endl;
						return false;
					}
					
					node->assignment(PTR, find);
					memset(name, '\0', n_len);
					delete name;
				}
			}
			
			else if (IS_OPER(POS)) {
				if(*POS == '[') {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}
				if(node->type == CHR) {
					if(*POS != '+') {
						std::cout << "You can't do anything except \"add\"" << std::endl;
						return false;
					}

					char *result;
					result = new char[node->size];
					mystrcpy(result, (char*)node->value, strlen((char*)node->value));
					result = string_proc(result, node->size);
					std::cout << '"' << result << '"' << std::endl;
					memset(result, '\0', strlen(result));
					delete result;
				}
				
				else if(node->type == INTEGER) {
					if(*POS == '[') {
						std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
						return false;
					}
					std::cout << '"' << arithmetic(node->value[0]) << '"' << std::endl;
				}

				else if(node->type == PTR) {
					std::cout << "ERROR: Pointer cannot be operated.." << std::endl;
					return false;
				}
			}
			
			else if(*POS == ';') {
				if(node->type == INTEGER) {
					std::cout << '"' << node->value[0] << '"' << std::endl;
				}
				
				else if(node->type == CHR) {
					std::cout << '"';
					iostream::write((char*)node->value, node->size);
					std::cout << '"' << std::endl;
				}

				else {
					std::cout << "ERROR: Unexpected variable type..." << std::endl;
					return false;
				}
			}
		}
		memset(data_type, '\0', type_len);
		delete data_type;
	}
	
	else {
		char *var_name;
		size_t name_len;
		char *save_pos;
		variable* node = HEAD;
		__int64_t result = 0;

		save_pos = POS;

		for(POS;;++POS) {
			if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
		}

		name_len = POS - save_pos;
		var_name = new char[name_len];
		memcpy(var_name, save_pos, name_len);
		while(node->next) {
			node = node->next;
			if(strcmp(node->name, var_name) == 0) break;
		}

		if(strcmp(node->name, var_name) != 0) {
			std::cout << "ERROR: unexpected token..." << std::endl;
			return false;
		}

		check_space();
		
		memset(var_name, '\0', name_len);
		delete var_name;

		if(*POS == '=') {
			save_pos = POS;
			char *save;
			char *name;
			size_t n_len;
			size_t ref_cnt = 0;
			variable *find = HEAD;
			*POS = '+';
			++POS;
			check_space();
			
			if((*POS <= '9' && *POS >= '0') || (*POS == '+' || *POS == '-')) {
				size_t assignment_size = node->size;
				if(node->type == CHR) assignment_size /= 8;
				POS = save_pos;
				node->assignment(INTEGER, arithmetic(0), 0, assignment_size);
			}

			else if (*POS == '"') {
				POS = save_pos;
				char *result = string_proc((char*)malloc(0x400), 0);
				size_t assignment_size = node->size;
				if(node->type != CHR) assignment_size *= 8;
				node->assignment(CHR, result, 0, assignment_size);
				memset(result, '\0', strlen(result));
				delete result;
			}

			else if (*POS == '*') {
				for(POS;;++POS) {
					if(*POS == '*') ++ref_cnt;
					else if(*POS == ' ');
					else if(*POS == '&') --ref_cnt;
					else break;
				}
				save = POS;
				for(POS;;++POS) {
					if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
				}
				n_len = POS - save;
				name = new char[n_len];
				memcpy(name, save, n_len);
				check_space();
				while(find->next) {
					find = find->next;
					if(strcmp(find->name, name) == 0) break;
				}

				if(strcmp(find->name, name) != 0) {
					std::cout << "ERROR: unexpected token..." << std::endl;
					return false;
				}

				memset(name, '\0', n_len);
				delete name;

				for(int i = 0;i < ref_cnt; ++i) {
					if(find->type != PTR) {
						std::cout << "You can't reference anything except pointer...!!" << std::endl;
						return false;
					}
					else if ((variable*)find->value[0] == NULL) {
						std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
						return false;
					}
					if(find->is_ref == true) {
						std::cout << "You can reference ptr just one time...!" << std::endl;
						return false;
					}
					find->is_ref = true;
					find = (variable*)(find->value[0]);
				}

				if(find->type == INTEGER) {
					POS = save_pos;	
					node->assignment(INTEGER, arithmetic(0), 0, find->size);
				}
				else if (find->type == CHR) {
					POS = save_pos;
					char *result = string_proc((char*)malloc(0x400), 0);
					node->assignment(CHR, result, 0, find->size);
					memset(result, '\0', strlen(result));
					delete result;
				}
				else if(find->type == PTR) {
					node->assignment(PTR, (variable*)find->value[0]);
				}
			}

			else if (*POS == '&') {
				char *name;
				size_t n_len;
				variable *find = HEAD;
				++POS;
				check_space();
				save = POS;
				for(POS;;++POS) {
					if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
				}
				n_len = POS - save;
				name = new char[n_len];
				memcpy(name, save_pos, n_len);
				while(find->next) {
					find = find->next;
					if(strcmp(find->name, name) == 0) break;
				}
				
				if(strcmp(find->name, name) != 0) {
					std::cout << "ERROR: unexpected token..." << std::endl;
					return false;
				}
				node->assignment(PTR, find);
				memset(name, '\0', n_len);
				delete name;
			}
		}
		
		else if (IS_OPER(POS)) {
			if(*POS == '[') {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}
			if(node->type == CHR) {
				if(*POS != '+') {
					std::cout << "You can't do anything except \"add\"" << std::endl;
					return false;
				}

				char *result;
				result = new char[node->size];
				mystrcpy(result, (char*)node->value, strlen((char*)node->value));
				result = string_proc(result, node->size);
				std::cout << '"' << result << '"' << std::endl;
				memset(result, '\0', strlen(result));
				delete result;
			}
			
			else if(node->type == INTEGER) {
				if(*POS == '[') {
					std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
					return false;
				}
				std::cout << '"' << arithmetic(node->value[0]) << '"' << std::endl;
			}

			else if(node->type == PTR) {
				std::cout << "ERROR: Pointer cannot be operated.." << std::endl;
				return false;
			}
		}
		
		else if(*POS == ';') {
			if(node->type == INTEGER) {
				std::cout << '"' << node->value[0] << '"' << std::endl;
			}
			
			else if(node->type == CHR) {
				std::cout << '"';
				iostream::write((char*)node->value, node->size);
				std::cout << '"' << std::endl;
			}

			else {
				std::cout << "ERROR: Unexpected variable type..." << std::endl;
				return false;
			}
		}
	}
	POS += 1;
	interprete(POS);
}

__int64_t arithmetic(__int64_t sum) {
	__int64_t value;
	char ch = *POS;
	if(ch == ';') return sum;

	if(IS_OPER(POS)) {
		if(ch == '[' || ch == '=') { 
			std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
			exit(-1);
		}
		POS += 1;
		check_space();
		if(*POS <= '9' && *POS >= '0' || (*POS == '+' || *POS == '-')) { 
			value = atol(POS);
			if(*POS == '+' || *POS == '-') POS += 1;
			switch(ch) { 
				case '+' :
					sum += value;
					break;
				case '-' :
					sum -= value;
					break;
				case '*' :
					sum *= value;
					break;
				case '/' :
					sum /= value;
					break;
				case '%' :
					sum %= value;
					break;
				default :
					std::cout << "??????" << std::endl;
					exit(-1);
			}
			for(POS;;++POS) {
				if(*POS > '9' || *POS <'0') break;
			}
			check_space();
		}
		else if(*POS == '*') {
			char *save_pos;
			char *var_name;
			size_t name_len;
			size_t ref_cnt = 0;
			variable *node = HEAD;
			for(POS;;++POS) {
				if(*POS == '*') ++ref_cnt;
				else if(*POS == ' ');
				else if(*POS == '&') --ref_cnt;
				else break;
			}
			save_pos = POS;
			
			if(ref_cnt < 0){
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				return false;
			}

			if(*POS <= '9' && *POS >= '0') {
				std::cout << "You can't reference number.." << std::endl;
				exit(-1);
			}

			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			if(*POS == '[') { 
				std::cout << "Pointer array does not exist...~~" << std::endl;
				exit(-1);
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) break;
			}
			
			if(strcmp(node->name, var_name) != 0) {
				std::cout << "This variable does not exist...!" << std::endl;
				exit(-1);
			}

			for(int i = 0;i < ref_cnt; ++i){
				if(node->type != PTR) {
					std::cout << "You can't reference anything except pointer...!!" << std::endl;
					exit(-1);
				}
				else if ((variable*)node->value[0] == NULL) {
					std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
					exit(-1);
				}
				if(node->is_ref == true) {
					std::cout << "You can reference ptr just one time...!" << std::endl;
					exit(-1);
				}
				node->is_ref = true;
				node = (variable*)(node->value[0]);
			}

			if(node->type != INTEGER) {
				std::cout << "You can't add anything except integer type!" << std::endl;
				exit(-1);
			}
			memset(var_name, '\0', name_len);
			delete var_name;

			switch(ch) {
				case '+' :
					sum += node->value[0];
					break;
				case '-' :
					sum -= node->value[0];
					break;
				case '*' :
					sum *= node->value[0];
					break;
				case '/' :
					sum /= node->value[0];
					break;
				case '%' :
					sum %= node->value[0];
					break;
				default :
					std::cout << "??????" << std::endl;
					exit(-1);
			}
		}

		else {
			char *save_pos = POS;
			char *var_name;
			variable*node = HEAD;
			size_t name_len;
			int arr_size = 0;
			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}
			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);
			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) break;
			}

			if(strcmp(node->name, var_name) != 0) {
				std::cout << "This variable does not exist...!" << std::endl;
				exit(-1);
			}
			if(node->type != INTEGER) {
				std::cout << "You can't add anything except integer type!" << std::endl;
				exit(-1);
			}
			if(*POS == '[') {
				if(node->is_arr == false) {
					std::cout << "hmm..? why do you do.." << std::endl;
					exit(-1);
				}
				else {
					POS += 1;
					check_space();
					save_pos = POS;
					if(*POS == '-') {
						std::cout << "Out Of Boundary check!" << std::endl;
						exit(-1); 
					}
					for(int i = 0; i < 4; ++i) { 
						if(*POS == ']') break;
						else if(*POS > '9' || *POS <'0') {
							std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
							exit(-1);
						}
						++POS;
					}
					if(*POS != ']') {
						std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
						exit(-1);
					}
					arr_size = atol(save_pos);
					POS += 1;
					check_space();
					if(arr_size >= node->size) {
						std::cout << "Out Of Boundary check!" << std::endl;
						exit(-1); 
					}
				}
			}
			switch(ch) {
				case '+' :
					sum += node->value[arr_size];
					break;
				case '-' :
					sum -= node->value[arr_size];
					break;
				case '*' :
					sum *= node->value[arr_size];
					break;
				case '/' :
					sum /= node->value[arr_size];
					break;
				case '%' :
					sum %= node->value[arr_size];
					break;
				default :
					std::cout << "??????" << std::endl;
					exit(-1);
			}
			memset(var_name, '\0', name_len);
			delete var_name;
		}
	}

	else {
		std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
		exit(-1);
	}
	arithmetic(sum);
}

char * string_proc(char *sum, size_t len) {
	if(*POS == ';') return sum;
	
	char *local_str = NULL;
	size_t local_len = 0;
	char *save_str = sum;

	if(IS_OPER(POS)) {
		if(*POS != '+') { 
			std::cout << "You can't do anything except \"add\"" << std::endl;
			exit(-1);
		}

		POS += 1; 
		check_space(); 

		if (*POS >= '0' && *POS <= '9') { 
			std::cout << "You can't add num at string...." << std::endl;
			exit(-1);
		}

		else if(*POS == '"') { 

			POS += 1;
			local_str = strchr(POS, '"');
			
			if(local_str == NULL) {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				exit(-1);
			}

			local_len = local_str - POS;
			local_str = new char[local_len];
			memcpy((void *)local_str, (const void *)POS, local_len);
			POS += local_len + 1;
			
			check_space();

			sum = new char[len + local_len]; 
			memcpy((void *)sum, (const void *)save_str, len);.
			memcpy((void *)(&sum[len]), (const void *)local_str, local_len);

			memset((void *)local_str, '\0', local_len);
			memset((void *)save_str, '\0', len);
			delete local_str;
			delete save_str;
		}

		else if(*POS == '*') {
			char *save_pos;
			char *var_name;
			size_t name_len;
			size_t ref_cnt = 0;
			variable *node = HEAD;
			for(POS;;++POS) {
				if(*POS == '*') ++ref_cnt;
				else if(*POS == ' ');
				else if(*POS == '&') --ref_cnt;
				else break;
			}

			save_pos = POS;
			if(ref_cnt < 0) {
				std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
				exit(-1);
			}

			if(*POS <= '9' && *POS >= '0') {
				std::cout << "You can't reference number.." << std::endl;
				exit(-1);
			}

			for(POS;;++POS) {
				if(*POS == ' ' || *POS == ';' || IS_OPER(POS)) break;
			}

			if(*POS == '[') { 
				std::cout << "Pointer array does not exist...~~" << std::endl;
				exit(-1);
			}

			name_len = POS - save_pos;
			var_name = new char[name_len];
			memcpy(var_name, save_pos, name_len);

			while(node->next) {
				node = node->next;
				if(strcmp(node->name, var_name) == 0) break;
			}
			
			if(strcmp(node->name, var_name) != 0) {
				std::cout << "This variable does not exist...!" << std::endl;
				exit(-1);
			}

			for(int i = 0; i < ref_cnt; ++i){
				if(node->type != PTR) {
					std::cout << "You can't reference anything except pointer...!!" << std::endl;
					exit(-1);
				}

				else if ((variable*)node->value[0] == NULL) {
					std::cout << "ERROR: NULL Pointer Exception!" << std::endl;
					exit(-1);
				}

				if(node->is_ref == true) {
					std::cout << "You can reference ptr just one time...!" << std::endl;
					exit(-1);
				}
				node->is_ref = true;
				node = (variable*)(node->value[0]);
			}

			if(node->type != CHR) {
				std::cout << "You can't add anything except Character type!" << std::endl;
				exit(-1);
			}
			memset(var_name, '\0', name_len);
			delete var_name;

			sum = new char [node->size + len];
			memcpy(sum, save_str, len);
			memcpy(&sum[len], node->value, node->size);

			memset(save_str, '\0', len);
			delete save_str;
		}

		else { 
			char *save_pos = POS; 
			size_t arr_size = 0;
			size_t n_len;
			char *name;
			bool is_indexing = false;
			variable *node = HEAD;

			for (POS;;++POS) {
				if(*POS == ' ' || IS_OPER(POS) || *POS == ';') break;
			} 
			
			n_len = POS - save_pos;
			name = new char[n_len];

			memcpy((void *)name, (const void *)save_pos, n_len);
			
			check_space();

			while (node->next != NULL) {
				node = node->next;
				if(strcmp(node->name, name) == 0) break;
			} 

			if(strcmp(node->name, name) != 0) {
				std::cout << "This variable does not exist...!" << std::endl;
				exit(-1);
			} 

			if(node->type != CHR) {
				std::cout << "You can't add anything except Character type!!" << std::endl; 
				exit(-1);	
			}

			memset(name, '\0', n_len);
			delete name; 

			if(*POS == '[') { 
				if(node->is_arr == false) { 
					std::cout << "hmm..? why do you do.." << std::endl;
					exit(-1);
				}

				else {
					is_indexing = true;
					POS += 1;
					check_space();
					save_pos = POS;
					if(*POS == '-') {
						std::cout << "Out Of Boundary check!" << std::endl;
						exit(-1); 
					}
					for(int i = 0; i < 4; ++i) { 
						if(*POS == ']') break;
						else if(*POS > '9' || *POS <'0') {
							std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
							exit(-1);
						}
						++POS;
					}
					if(*POS != ']') {
						std::cout << "You need to fit to interpreter's syntax..!" << std::endl;
						exit(-1);
					}

					arr_size = atol(save_pos);
					POS += 1;
					check_space();
					if(arr_size >= node->size) {
						std::cout << "Out Of Boundary check!" << std::endl;
						exit(-1); 
					}
				}
			}

			if(is_indexing == false && node->is_arr == true) { 
				local_str = new char[node->size];
				sum = new char[node->size + len];
				memcpy(local_str, node->value, node->size);
				memcpy(sum, save_str, len); 
				memcpy(&sum[len], local_str, node->size); 
			}

			else {
				sum = new char[1 + len];
				memcpy(sum, save_str, len);
				sum[len] = node->value[arr_size];
			}

			memset(save_str, '\0', len);
			delete save_str;

			if(local_str != NULL) {
				memset(local_str, '\0', node->size);
				delete local_str;
			}
			check_space();
		}
	}
	string_proc(sum, local_len + len);
}