#include "bf.h"

int bf_interpret(char *code, int code_size, int buf_size) {
  char *buffer, *cur, *ptr, *result, *out;

  if (bf_validate(code, code_size)) {
    return 1;
  }

  buffer = calloc(buf_size, 1);
  result = calloc(code_size, 1);
  cur = buffer;
  ptr = code;
  out = result;

  while (*ptr != 0) {
    if (!(buffer <= cur && cur < buffer + buf_size)) return 1;
    char c = *ptr;
    switch(c) {
    case '>': ++cur; break;
    case '<': --cur; break;
    case '+': (*cur)++; break;
    case '-': (*cur)--; break;
    case ',': *cur = getchar(); break;
    case '.': *out = *cur; out++; break;
    case '[':
      if (*cur == '\0') {
        while(*(++ptr) != ']');
      }
      break;
    case ']':
      if (*cur != '\0') {
        while(*(--ptr) != '[');
      }
      break;
    }
    ++ptr;
  }

  puts(result);

  free(buffer);
  free(result);
  return 0;
}

int bf_validate(char *code, int size) {
  char *ptr = code;
  int num_cb = 0;
  int num_ob = 0;
  int i;
  
  for(i = 0; (i < size) && (*ptr != 0); i++, ptr++) {
    char c = *ptr;
    switch(c) {
    case '>':
    case '<':
    case '+':
    case '-':
    case '.':
    case ',':
      break;
    case '[':
      num_ob++;
      break;
    case ']':
      num_cb++;
      break;
    default:
      return 1;
    }
  }

  if (num_cb != num_ob) return 1;
  
  return 0;
}
