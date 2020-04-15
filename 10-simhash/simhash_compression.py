from bitarray import bitarray


def compress(buf, a, b):
    n = (a^b).bit_length()
    offset = 64 - n
    for i in xrange(5, -1, -1):
        buf.append(offset & (1 << i) )
    for i in range(n-2, -1, -1):
        buf.append((b & ( 1 << i )))

def decompress(buf, a):
    offset = 0
    for i in range(0,6):
        offset |= buf.pop(0) << (5 - i)
    num_bits = 64 - offset - 1

    hsb = a

    if num_bits >= 0:
        hsb ^= 1 << num_bits
        for i in range(0,num_bits):
            hsb |= buf.pop(0) << (num_bits - i -1)

    return hsb

if __name__ == '__main__':
    buf = bitarray()
    sa = 0b010000010101110010111010110000101010001010001001001001000101001
    sb = 0b010000010101110010111010110000101010001010001001001001000011001
    for i in range(0,64):
        buf.append(sa & 1 << (63-i))
    compress(buf, sa, sb)

    hsa = 0
    for i in range(0,64):
        hsa |= buf.pop(0) << (63-i)

    hsb = decompress(buf, hsa)

    print buf