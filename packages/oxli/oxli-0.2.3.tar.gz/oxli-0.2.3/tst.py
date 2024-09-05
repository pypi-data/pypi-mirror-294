import oxli

kmer = 'TAAACCCTAACCCTAACCCTAACCCTAACCC'

cg = oxli.KmerCountTable(ksize=31)
hashkey = cg.hash_kmer(kmer)

assert cg.get(kmer) == 0
assert cg.count(kmer) == 1
assert cg.count(kmer) == 2

x = cg.get(kmer)
assert x == 2, x
