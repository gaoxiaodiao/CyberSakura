int read2(int in, char *buf, int size)
{
  for(int i = 0; i < size;) {
    if (i > 0x100) break;
    int readBytes = read(in, buf[i], size - i);
    if (readBytes == 0) {
      exit(1);
    }
    i += readBytes;
  }
}

void read_until_delim(int pipe, char *buffer, int size, char delim)
{
  
}

void child_worker(int c2p, int p2c) {
  read_until_delim(c2p, buffer, 0x20, '\x0a');
  
}

void main(void)
{
  int pipe_p2c[2], pipe_c2p[2];
  pipe(pipe_p2c);
  pipe(pipe_c2p);
  int pid = fork();
  if (pid < 0) {
    return;
  } else if (pid == 0) {
    /* Child */
    close(pipe_c2p[0]);
    close(pipe_p2c[1]);
    child_worker(pipe_c2p[1], pipe_p2c[0]);
  } else {
    /* Parent */
    close(pipe_c2p[1]);
    close(pipe_p2c[0]);
    parent_worker(pipe_c2p[0], pipe_p2c[1]);
  }
}
