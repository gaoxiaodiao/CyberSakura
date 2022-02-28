__int64 __fastcall MyCheapVM::exec(MyCheapVM *this)
{
  __int64 code; // rcx
  int v2; // edx
  __int64 result; // rax
  int v4; // eax
  int v5; // eax

  code = this->code;
  pc = this->pc;
  switch ( *(_BYTE *)(code + this->pc) )
  {
    case 0x10:
      this->regs[code[pc+1]] = this->regs[code[pc+2]];
      return result;
    case 0x11:
      this->regs[code[pc+1]] = code[pc+2:pc+6];
      return result;
    case 0x20:
      this->regs[code[pc+1]] &= this->regs[code[pc+2]];
      return result;
    case 0x21:
      this->regs[code[pc+1]] &= code[pc+2:pc+6];
      return result;
    case 0x22:
      this->regs[code[pc+1]] |= this->regs[code[pc+2]];
      return result;
    case 0x23:
      this->regs[code[pc+1]] |= code[pc+2:pc+6];
      return result;
    case 0x24:
      this->regs[code[pc+1]] ^= this->regs[code[pc+2]];
      return result;
    case 0x25:
      this->regs[code[pc+1]] ^= code[pc+2:pc+6];
      return result;
  case 0x30: // kokomade ok
      this->regs[code[pc+1]] = ~*((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)));
      return result;
    case 0x40:
      goto jmp2reg;
    case 0x41:
      goto LABEL_3;
    case 0x42:
      if ( this->sf )
        goto skip1;
      goto jnz_reg;
    case 0x43:
      if ( this->sf )
        goto LABEL_12;
      goto jnz_imm;
    case 0x44:
      result = this->sf;
      if ( (_BYTE)result )
        goto jmp2reg;
      goto skip2;
    case 0x45:
      result = this->sf;
      if ( (_BYTE)result )
        goto LABEL_3;
      goto LABEL_34;
    case 0x46:
      result = this->zf;
      if ( (_BYTE)result )
      {
jmp2reg:
        this->pc = this->regs[code[pc+1]];
        result = 0LL;
      }
      else
      {
skip2:
        this->pc = pc + 2;
      }
      break;
    case 0x47:
      result = this->zf;
      if ( (_BYTE)result )
      {
LABEL_3:
        this->pc = *(_DWORD *)(code + (unsigned int)(pc + 1));
        result = 0LL;
      }
      else
      {
LABEL_34:
        this->pc = pc + 5;
      }
      break;
    case 0x48:
jnz_reg:
      result = this->zf;
      if ( (_BYTE)result )
      {
skip1:
        result = 0LL;
        this->pc = pc + 2;
      }
      else
      {
        this->pc = this->regs[code[pc+1]];
      }
      break;
    case 0x49:
jnz_imm:
      result = this->zf;
      if ( (_BYTE)result )
      {
LABEL_12:
        result = 0LL;
        this->pc = pc + 5;
      }
      else
      {
        this->pc = *(_DWORD *)(code + (unsigned int)(pc + 1));
      }
      break;
    case 0x50:
      this->regs[code[pc+1]] += this->regs[code[pc+2]];
      break;
    case 0x51:
      this->regs[code[pc+1]] += code[pc+2:pc+6];
      break;
    case 0x52:
      this->regs[code[pc+1]] -= this->regs[code[pc+2]];
      break;
    case 0x53:
      this->regs[code[pc+1]] -= code[pc+2:pc+6];
      break;
    case 0x60:
      v5 = this->regs[code[pc+1]]
         - this->regs[code[pc+2]];
      this->delta = v5;
      if ( v5 < 0 )
        *((_WORD *)this + 34) = 1;
      else
        *((_WORD *)this + 34) = (v5 == 0) << 8;
      break;
    case 0x61:
      v4 = this->regs[code[pc+1]]
         - code[pc+2:pc+6];
      this->delta = v4;
      if ( v4 < 0 )
        *((_WORD *)this + 34) = 1;
      else
        *((_WORD *)this + 34) = (v4 == 0) << 8;
      break;
    case 0xFF:
      result = 1LL;
      break;
    default:
      std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "System error due to unknown instruction.", 40LL);
      std::endl<char,std::char_traits<char>>(&std::cout);
      exit(1);
      return result;
  }
  return result;
}
