__author__ = 'pwq'
#-*- coding: utf-8 -*-
def deal_str(str):
    len_num = len(str)
    if len_num<2:

        return True
    for i in range(len_num):
        for j in range(i+1,len_num):
            if str[i]==str[j]:
                if deal_str(str[i+1:j]):
                    print "___________",i,j
                    print str
                    return True
                else:
                    continue
            else:
                return False

a = "abccbaddjaca"
all_len = len(a)
for i in range(all_len):
    for j in range(i+1,all_len):
        if a[i]==a[j]:
            deal_str(a[i+1:j])

