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
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) = *((_DWORD *)this
                                                                              + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      return result;
    case 0x11:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) = *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc += 6;
      return result;
    case 0x20:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) &= *((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      return result;
    case 0x21:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) &= *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc = pc + 6;
      return result;
    case 0x22:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) |= *((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      return result;
    case 0x23:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) |= *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc = pc + 6;
      return result;
    case 0x24:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) ^= *((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      return result;
    case 0x25:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) ^= *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc = pc + 6;
      return result;
    case 0x30:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) = ~*((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)));
      result = 0LL;
      this->pc = pc + 2;
      return result;
    case 0x40:
      goto LABEL_5;
    case 0x41:
      goto LABEL_3;
    case 0x42:
      if ( *((_BYTE *)this + 68) )
        goto LABEL_14;
      goto LABEL_8;
    case 0x43:
      if ( *((_BYTE *)this + 68) )
        goto LABEL_12;
      goto LABEL_6;
    case 0x44:
      result = *((unsigned __int8 *)this + 68);
      if ( (_BYTE)result )
        goto LABEL_5;
      goto LABEL_36;
    case 0x45:
      result = *((unsigned __int8 *)this + 68);
      if ( (_BYTE)result )
        goto LABEL_3;
      goto LABEL_34;
    case 0x46:
      result = *((unsigned __int8 *)this + 69);
      if ( (_BYTE)result )
      {
LABEL_5:
        this->pc = *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)));
        result = 0LL;
      }
      else
      {
LABEL_36:
        this->pc = pc + 2;
      }
      break;
    case 0x47:
      result = *((unsigned __int8 *)this + 69);
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
LABEL_8:
      result = *((unsigned __int8 *)this + 69);
      if ( (_BYTE)result )
      {
LABEL_14:
        result = 0LL;
        this->pc = pc + 2;
      }
      else
      {
        this->pc = *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)));
      }
      break;
    case 0x49:
LABEL_6:
      result = *((unsigned __int8 *)this + 69);
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
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) += *((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      break;
    case 0x51:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) += *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc = pc + 6;
      break;
    case 0x52:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) -= *((_DWORD *)this
                                                                               + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      result = 0LL;
      this->pc = pc + 3;
      break;
    case 0x53:
      *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1))) -= *(_DWORD *)(code + (unsigned int)(pc + 2));
      result = 0LL;
      this->pc = pc + 6;
      break;
    case 0x60:
      v5 = *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)))
         - *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 2)));
      *((_DWORD *)this + 18) = v5;
      if ( v5 < 0 )
        *((_WORD *)this + 34) = 1;
      else
        *((_WORD *)this + 34) = (v5 == 0) << 8;
      result = 0LL;
      this->pc = pc + 3;
      break;
    case 0x61:
      v4 = *((_DWORD *)this + *(unsigned __int8 *)(code + (unsigned int)(pc + 1)))
         - *(_DWORD *)(code + (unsigned int)(pc + 2));
      *((_DWORD *)this + 18) = v4;
      if ( v4 < 0 )
        *((_WORD *)this + 34) = 1;
      else
        *((_WORD *)this + 34) = (v4 == 0) << 8;
      result = 0LL;
      this->pc = pc + 6;
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
