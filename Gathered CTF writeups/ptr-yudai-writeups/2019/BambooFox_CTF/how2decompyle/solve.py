table = 'abcdefghijklmnopqrstuvwxyz_'

restrictions = [
    'uudcjkllpuqngqwbujnbhobowpx_kdkp_',
    'f_negcqevyxmauuhthijbwhpjbvalnhnm',
    'dsafqqwxaqtstghrfbxzp_x_xo_kzqxck',
    'mdmqs_tfxbwisprcjutkrsogarmijtcls',
    'kvpsbdddqcyuzrgdomvnmlaymnlbegnur',
    'oykgmfa_cmroybxsgwktlzfitgagwxawu',
    'ewxbxogihhmknjcpbymdxqljvsspnvzfv',
    'izjwevjzooutelioqrbggatwkqfcuzwin',
    'xtbifb_vzsilvyjmyqsxdkrrqwyyiu_vb',
    'watartiplxa_ktzn_ouwzndcrfutffyzd',
    'rqzhdgfhdnbpmomakleqfpmxetpwpobgj',
    'qggdzxprwisr_vkkipgftuvhsizlc_pbz',
    'jerzhlnsegcaqzathfpuufwunakdtceqw',
    'lbvlyyrugffgrwo_v_zrqvqszchqrrljq',
    'aiwuuhzbszvfpidwwkl_wynlujbsbhfox',
    'vmhrizxtiegxdxsqcdoiyxkffloudwtxg',
    'tffjnabob_jbf_qiszdsemczghnjysmah',
    'zrqkppvynlkelnevngwlkhgaputhoagtt',
    'nl_oojyafwoqccbedijmigpedkdzglq_f',
    'cksy_skctjlyxktuzchvstunyvcvabomc',
    'ppcxleeguvhvhengmvac_bykhzqohjuei',
    '_clmaicjrrzhwd_fescyaejtbyefxyihy',
    'hhopvwsmjtpjiffzatyhjrev_dwnsidyo',
    'sjevtrmkkk_zjalxrxfovjsbcxjx_pskp',
    'gnynwuuqypddbsylparpcczqimimqmvdl',
    'bxitcmhnmanwuhvjxnqeoiimlegrmkjra']

flag = ''
for i in range(len(restrictions[0])):
    for c in table:
        for restriction in restrictions:
            if c == restriction[i]:
                break
        else:
            flag += c

print(flag)
