bool __fastcall MyCheapVM::check(MyCheapVM *this, char *a2)
{
  unsigned int pc; // edx
  __int64 code; // rcx
  bool result; // al
  int v5; // eax
  int v6; // eax
  __int64 v7; // rax
  __int64 v8; // r8
  __int64 v9; // rax
  __int64 v10; // r8
  __int64 v11; // rax
  __int64 v12; // r8
  __int64 v13; // rax
  __int64 v14; // r8
  __int64 v15; // rax
  __int64 v16; // rax
  __int64 v17; // r8
  __int64 v18; // rax
  __int64 v19; // r8
  __int64 v20; // rax
  __int64 v21; // r8
  __int64 v22; // rax
  __int64 v23; // r8
  __int64 v24; // rax
  __int64 v25; // r8
  __int64 v26; // rax
  __int64 v27; // r8
  int v28; // er8
  __int64 v29; // rax

  if ( a2 < (char *)this + 16 && this < (MyCheapVM *)(a2 + 16) )
  {
    *(_DWORD *)this = *(_DWORD *)a2;
    *((_DWORD *)this + 1) = *((_DWORD *)a2 + 1);
    *((_DWORD *)this + 2) = *((_DWORD *)a2 + 2);
    *((_DWORD *)this + 3) = *((_DWORD *)a2 + 3);
    *((_DWORD *)this + 4) = *((_DWORD *)a2 + 4);
    *((_DWORD *)this + 5) = *((_DWORD *)a2 + 5);
    *((_DWORD *)this + 6) = *((_DWORD *)a2 + 6);
    *((_DWORD *)this + 7) = *((_DWORD *)a2 + 7);
  }
  else
  {
    *(__m128i *)this = _mm_loadu_si128((const __m128i *)a2);
    *((__m128i *)this + 1) = _mm_loadu_si128((const __m128i *)a2 + 1);
  }
  pc = *((_DWORD *)this + 16);
  code = *((_QWORD *)this + 10);
  while ( 1 )
  {
    switch ( *(_BYTE *)(code + pc) )
    {
      case 0x10:
        v28 = *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 2));
        v29 = pc + 1;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v29)) = v28;
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x11:
        *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 1)) = *(_DWORD *)(code + pc + 2);
        code = *((_QWORD *)this + 10);
        pc = *((_DWORD *)this + 16) + 6;
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x20:
        v26 = pc + 1;
        v27 = pc + 2;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v26)) &= *((_DWORD *)this + *(unsigned __int8 *)(code + v27));
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x21:
        v24 = pc + 1;
        v25 = pc + 2;
        pc += 6;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v24)) &= *(_DWORD *)(code + v25);
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x22:
        v22 = pc + 1;
        v23 = pc + 2;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v22)) |= *((_DWORD *)this + *(unsigned __int8 *)(code + v23));
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x23:
        v20 = pc + 1;
        v21 = pc + 2;
        pc += 6;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v20)) |= *(_DWORD *)(code + v21);
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x24:
        v18 = pc + 1;
        v19 = pc + 2;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v18)) ^= *((_DWORD *)this + *(unsigned __int8 *)(code + v19));
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x25:
        v16 = pc + 1;
        v17 = pc + 2;
        pc += 6;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v16)) ^= *(_DWORD *)(code + v17);
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x30:
        v15 = pc + 1;
        pc += 2;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v15)) = ~*((_DWORD *)this + *(unsigned __int8 *)(code + v15));
        *((_DWORD *)this + 16) = pc;
        continue;
      case 0x40:
        goto LABEL_11;
      case 0x41:
        goto LABEL_8;
      case 0x42:
        if ( !*((_BYTE *)this + 68) )
          goto LABEL_10;
        goto LABEL_13;
      case 0x43:
        if ( !*((_BYTE *)this + 68) )
          goto LABEL_7;
        goto LABEL_15;
      case 0x44:
        if ( !*((_BYTE *)this + 68) )
          goto LABEL_13;
        goto LABEL_11;
      case 0x45:
        if ( !*((_BYTE *)this + 68) )
          goto LABEL_15;
        pc = *(_DWORD *)(code + pc + 1);
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x46:
        if ( !*((_BYTE *)this + 69) )
          goto LABEL_13;
        pc = *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 1));
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x47:
        if ( !*((_BYTE *)this + 69) )
          goto LABEL_15;
        goto LABEL_8;
      case 0x48:
LABEL_10:
        if ( *((_BYTE *)this + 69) )
        {
LABEL_13:
          pc += 2;
          *((_DWORD *)this + 16) = pc;
        }
        else
        {
LABEL_11:
          pc = *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 1));
          *((_DWORD *)this + 16) = pc;
        }
        break;
      case 0x49:
LABEL_7:
        if ( *((_BYTE *)this + 69) )
        {
LABEL_15:
          pc += 5;
          *((_DWORD *)this + 16) = pc;
        }
        else
        {
LABEL_8:
          pc = *(_DWORD *)(code + pc + 1);
          *((_DWORD *)this + 16) = pc;
        }
        break;
      case 0x50:
        v13 = pc + 1;
        v14 = pc + 2;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v13)) += *((_DWORD *)this + *(unsigned __int8 *)(code + v14));
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x51:
        v11 = pc + 1;
        v12 = pc + 2;
        pc += 6;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v11)) += *(_DWORD *)(code + v12);
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x52:
        v9 = pc + 1;
        v10 = pc + 2;
        pc += 3;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v9)) -= *((_DWORD *)this + *(unsigned __int8 *)(code + v10));
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x53:
        v7 = pc + 1;
        v8 = pc + 2;
        pc += 6;
        *((_DWORD *)this + *(unsigned __int8 *)(code + v7)) -= *(_DWORD *)(code + v8);
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x60:
        v6 = *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 1))
           - *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 2));
        *((_DWORD *)this + 18) = v6;
        if ( v6 < 0 )
          *((_WORD *)this + 34) = 1;
        else
          *((_WORD *)this + 34) = (v6 == 0) << 8;
        pc += 3;
        *((_DWORD *)this + 16) = pc;
        break;
      case 0x61:
        v5 = *((_DWORD *)this + *(unsigned __int8 *)(code + pc + 1)) - *(_DWORD *)(code + pc + 2);
        *((_DWORD *)this + 18) = v5;
        if ( v5 < 0 )
          *((_WORD *)this + 34) = 1;
        else
          *((_WORD *)this + 34) = (v5 == 0) << 8;
        pc += 6;
        *((_DWORD *)this + 16) = pc;
        break;
      case 0xFF:
        return *(_DWORD *)this != 0;
      default:
        std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "System error due to unknown instruction.", 40LL);
        std::endl<char,std::char_traits<char>>(&std::cout);
        exit(1);
        return result;
    }
  }
}
