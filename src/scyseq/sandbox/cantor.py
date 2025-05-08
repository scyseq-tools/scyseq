#(NS) def cantor_seq(l,N,k=2):
#    s=Num.zeros((N))
#    n=0
#    while (np.floor(N/pow(2,n)) > 0):
#     s[int(np.floor(N/pow(2,n))):int(np.floor(N/pow(2,n)+l*N/pow(2,n)))]=1
#     n = n + 1
#    print s
#    return Sequence(s=s, k=k)

#(NS) def cantor_it_g(seq,l,it):
#    seq.s[int(np.floor(seq.N/pow(2,it))):int(np.floor(seq.N/pow(2,it)+l*seq.N/pow(2,it)))]=1
#    return Sequence(s=seq.s, k=seq.k)

#(NS) def cantor_it_d(seq,l,it):
#    seq.s[-int(np.floor(seq.N/pow(2,it)+l*seq.N/pow(2,it))):-int(np.floor(seq.N/pow(2,it)))]=1
#    return Sequence(s=seq.s, k=seq.k)

