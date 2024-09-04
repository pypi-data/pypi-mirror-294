def rna_visualizations(sequence):
    top_strand = ''
    visualization = []
    l = len(sequence)
    for i in range(0, len(sequence), 15):
        end_index = min(i + 15, len(sequence))

        # TOP & BOTTOM STRANDS
        if i == 0 and end_index < l:
            top_strand = f"5'   {'-'.join(sequence[i:end_index])}—"
        elif i == 0 and end_index == len(sequence):
            top_strand = f"5'   {'-'.join(sequence[i:end_index])}   3'"
        elif i > 0 and end_index < len(sequence):
            top_strand = f"    —{'-'.join(sequence[i:end_index])}—"
        elif i > 0 and end_index == len(sequence):
            top_strand = f"    —{'-'.join(sequence[i:end_index])}   3'"

        # CONNECTORS
        connectors = f"     {' '.join('|' for _ in sequence[i:end_index])}   {end_index}"

        visualization.append(top_strand)
        visualization.append(connectors)
        visualization.append('')

    visualize = '\n'.join(visualization)
    return visualize


def dna_transcription(rna_sequence):
    trans_nucleotides = {'U': 'A', 'A': 'T', 'C': 'G', 'G': 'C'}
    dna_seq = ''.join(trans_nucleotides.get(base, base) for base in rna_sequence)
    return dna_seq[::-1]


def nucleotide_frequency(sequence):
    a = sequence.count('A')
    c = sequence.count('C')
    g = sequence.count('G')
    u = sequence.count('U')

    return (f'A: {a}\n'
            f'C: {c}\n'
            f'G: {g}\n'
            f'U: {u}\n')


def compute_gc_content_rna(sequence):
    length = len(sequence)
    if length == 0:
        raise ZeroDivisionError('The sequence is empty')
    gc = sum(1 for base in sequence if base in 'GC')
    return gc / length


def protein_transcription(sequence, steps):
    codons_dict = {
        'UUU': 'F', 'UCU': 'S', 'UAU': 'Y', 'UGU': 'C',
        'UUC': 'F', 'UCC': 'S', 'UAC': 'Y', 'UGC': 'C',
        'UUA': 'L', 'UCA': 'S', 'UAA': '-', 'UGA': '-',
        'UUG': 'L', 'UCG': 'S', 'UAG': '-', 'UGG': 'W',
        'CUU': 'L', 'CCU': 'P', 'CAU': 'H', 'CGU': 'R',
        'CUC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R',
        'CUA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R',
        'CUG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R',
        'AUU': 'I', 'ACU': 'T', 'AAU': 'N', 'AGU': 'S',
        'AUC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S',
        'AUA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R',
        'AUG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R',
        'GUU': 'V', 'GCU': 'A', 'GAU': 'D', 'GGU': 'G',
        'GUC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G',
        'GUA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G',
        'GUG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G'
    }

    protein = ''.join(codons_dict.get(sequence[i:i + 3], '') for i in range(0, len(sequence) - 2, steps))
    return protein


def most_frequent_kmer(sequence, k):
    frequencies = {}
    for i in range(len(sequence) - k + 1):
        substring = sequence[i:i + k]
        if substring in frequencies:
            frequencies[substring] += 1
        else:
            frequencies[substring] = 1

    frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return frequencies

