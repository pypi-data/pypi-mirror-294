def reverse_complement(sequence):
    complements = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    complement_seq = ''.join(complements.get(base) for base in sequence)
    reverse_complement_seq = complement_seq[::-1]
    return reverse_complement_seq


def compute_gc_content(sequence):
    length = len(sequence)
    if length == 0:
        raise ZeroDivisionError('The sequence is empty')
    gc = sum(1 for base in sequence if base in 'GC')
    return gc / length


def rna_transcription(sequence):
    trans_nucleotides = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C'}
    rna_seq = ''.join(trans_nucleotides.get(base, base) for base in sequence)
    return rna_seq[::-1]


def check_overlap(positions):
    x = 0
    for j in range(x, len(positions)):
        for i in range(x, len(positions) - 1):
            if positions[i][0] == positions[i + 1][0] \
                    or positions[i][1] == positions[i + 1][1] \
                    or positions[i + 1][0] <= positions[i][1]:
                del positions[i + 1]
                x = i
                break

    return positions


def define_start_stop_codons(sequence, length, overlap=True):
    start_codons = ['ATG']
    stop_codons = ['TAA', 'TAG', 'TGA']
    positions = []

    i = 0
    for i in range(0, length - 2):
        start = -1
        end = -1
        if sequence[i:i + 3] in start_codons:
            start = i
            for j in range(i, length - 2, 3):
                if sequence[j:j + 3] in stop_codons:
                    end = j + 3
                    positions.append((start, end))
                    break
    if not overlap:
        positions = check_overlap(positions)

    return positions


def protein_transcription(sequence, steps):
    codons_dict = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '-', 'TAG': '-',
        'TGT': 'C', 'TGC': 'C', 'TGA': '-', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }

    protein = ''.join(codons_dict.get(sequence[i:i + 3], '') for i in range(0, len(sequence) - 2, steps))
    return protein


def open_reading_frames(sequence):
    complements = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

    ori_seq = sequence
    ori_pos = define_start_stop_codons(ori_seq, len(ori_seq))
    rev_comp = reverse_complement(ori_seq)
    comp_pos = define_start_stop_codons(rev_comp, len(rev_comp))

    orf = []
    for pos in ori_pos:
        orf.append(ori_seq[pos[0]:pos[1]])
    for pos in comp_pos:
        orf.append(rev_comp[pos[0]:pos[1]])

    orf_prot = []
    for orf_seq in orf:
        protein = protein_transcription(orf_seq, steps=3)
        if protein not in orf_prot:
            orf_prot.append(protein)

    return orf_prot


def dna_visualization(sequence):
    rev_comp = reverse_complement(sequence)
    comp_seq = rev_comp[::-1]
    l = len(sequence)
    top_strand = ''
    bottom_strand = ''
    visualization = []

    for i in range(0, len(sequence), 15):
        end_index = min(i + 15, len(sequence))

        # TOP & BOTTOM STRANDS
        if i == 0 and end_index < l:
            top_strand = f"5'   {'-'.join(sequence[i:end_index])}—"
            bottom_strand = f"3'   {'-'.join(comp_seq[i:end_index])}—"
        elif i == 0 and end_index == len(sequence):
            top_strand = f"5'   {'-'.join(sequence[i:end_index])}   3'"
            bottom_strand = f"3'   {'-'.join(comp_seq[i:end_index])}   5'"
        elif i > 0 and end_index < len(sequence):
            top_strand = f"    —{'-'.join(sequence[i:end_index])}—"
            bottom_strand = f"    —{'-'.join(comp_seq[i:end_index])}—"
        elif i > 0 and end_index == len(sequence):
            top_strand = f"    —{'-'.join(sequence[i:end_index])}   3'"
            bottom_strand = f"    —{'-'.join(comp_seq[i:end_index])}   5'"

        # CONNECTORS
        connectors = f"     {' '.join('│' for _ in sequence[i:end_index])}   {end_index}"

        visualization.append(top_strand)
        visualization.append(connectors)
        visualization.append(bottom_strand)
        visualization.append('')

    visualize = '\n'.join(visualization)
    return visualize


def nucleotide_frequency(sequence):
    a = sequence.count('A')
    c = sequence.count('C')
    g = sequence.count('G')
    t = sequence.count('T')

    return (f'A: {a}\n'
            f'C: {c}\n'
            f'G: {g}\n'
            f'T: {t}\n')


def generate_dna(length=20):
    import random
    from myPackage.GeneMaster.dtypes.DNA import DNA

    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ''.join(random.choice(nucleotides) for _ in range(length))
    return DNA(sequence)


def extract_exon_parts(dna_sequence, exon_positions):
    exons = []
    exon_positions.sort()

    for start, end in exon_positions:
        exon = dna_sequence[start:end]
        exons.append(exon)
    spliced_sequence = ''.join(exons)

    return spliced_sequence


def extract_intron_parts(dna_sequence, exon_positions):
    introns = []
    last_exon_end = 0
    exon_positions.sort()

    for start, end in exon_positions:
        if start > last_exon_end:
            intron = dna_sequence[last_exon_end:start]
            introns.append(intron)
        last_exon_end = end
    if last_exon_end < len(dna_sequence):
        introns.append(dna_sequence[last_exon_end:])
    concatenated_introns = ''.join(introns)

    return concatenated_introns


def hamming_distance(seq1, seq2):
    if type(seq1) != type(seq2):
        raise TypeError('seq1 and seq2 must be of same type')
    hamming_distance = 0
    for i in range(min(len(seq1), len(seq2))):
        if seq1[i] != seq2[i]:
            hamming_distance += 1

    return hamming_distance


def find_motif_sequence(seq, motif):
    locations = []
    motif_len = len(motif)
    strand_len = len(seq)

    for i in range(strand_len - motif_len + 1):
        if seq[i:i + motif_len] == str(motif):
            start = i
            end = start + motif_len
            locations.append((start, end))

    return locations


def find_shared_motif(seqs_list, min_L=2, max_L=10):
    sorted_seqs_list = sorted(seqs_list, key=len)
    main_strand = sorted_seqs_list[0]
    motifs = []

    for i in range(len(main_strand)):
        for j in range(i + min_L, min(len(main_strand), max_L) + 1):
            subseq = main_strand[i:j]
            is_found = True
            for seq in sorted_seqs_list[1:]:
                if subseq not in seq:
                    is_found = False
                    break
            if is_found:
                if subseq not in motifs:
                    motifs.append(subseq)
    sorted_motifs = sorted(motifs)
    return sorted_motifs


def compute_melting_temperature(sequence, length):
    A, T, C, G = sequence.count('A'), sequence.count('T'), \
        sequence.count('C'), sequence.count('G')
    if length < 14:
        t_m = (C + G) * 4 + (A + T) * 2
    else:
        t_m = 64.9 + 41 * (C + G - 16.4) / (A + T + G + C)

    return t_m


def make_pairwise_align(seq1, seq2, match_score=1, mismatch_score=-1, gap_score=-1):
    import numpy as np

    num_rows = len(seq2) + 1
    num_cols = len(seq1) + 1

    score_matrix = np.zeros((num_rows, num_cols), dtype=int)
    direction_matrix = np.zeros((num_rows, num_cols), dtype=int)

    for i in range(1, num_rows):
        score_matrix[i, 0] = gap_score * i
        direction_matrix[i, 0] = 1

    for j in range(1, num_cols):
        score_matrix[0, j] = gap_score * j
        direction_matrix[0, j] = 2

    for i in range(1, num_rows):
        for j in range(1, num_cols):
            match = score_matrix[i - 1, j - 1] + (match_score if seq2[i - 1] == seq1[j - 1] else mismatch_score)
            delete = score_matrix[i - 1, j] + gap_score
            insert = score_matrix[i, j - 1] + gap_score
            score_matrix[i, j] = max(match, delete, insert)

            if score_matrix[i, j] == match:
                direction_matrix[i, j] = 0
            elif score_matrix[i, j] == delete:
                direction_matrix[i, j] = 1
            else:
                direction_matrix[i, j] = 2

    aligned_seq1 = []
    aligned_seq2 = []
    i, j = num_rows - 1, num_cols - 1

    while i > 0 or j > 0:
        if direction_matrix[i, j] == 0:
            aligned_seq1.append(seq1[j - 1])
            aligned_seq2.append(seq2[i - 1])
            i -= 1
            j -= 1
        elif direction_matrix[i, j] == 1:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[i - 1])
            i -= 1
        else:
            aligned_seq1.append(seq1[j - 1])
            aligned_seq2.append('-')
            j -= 1

    while i > 0:
        aligned_seq1.append('-')
        aligned_seq2.append(seq2[i - 1])
        i -= 1

    while j > 0:
        aligned_seq1.append(seq1[j - 1])
        aligned_seq2.append('-')
        j -= 1

    aligned_seq1.reverse()
    aligned_seq2.reverse()

    return ''.join(aligned_seq1), ''.join(aligned_seq2)


def compute_codon_bias(sequence):
    codons_dict = {}

    for i in range(len(sequence) - 2):
        if sequence[i:i + 3] in codons_dict:
            codons_dict[sequence[i:i + 3]] += 1
        else:
            codons_dict[sequence[i:i + 3]] = 1

    sorted_dict_desc = dict(sorted(codons_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict_desc


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


def overlap(a, b):
    max_overlap = 0
    min_length = min(len(a), len(b))

    for i in range(1, min_length + 1):
        if a[-i:] == b[:i]:
            max_overlap = i

    return max_overlap


def merge(a, b, overlap_len):
    return a + b[overlap_len:]


def shortest_superstring(dna_strands):
    overlap_matrix = {}
    n = len(dna_strands)

    for i in range(n):
        for j in range(n):
            if i != j:
                overlap_matrix[(i, j)] = overlap(dna_strands[i], dna_strands[j])

    while len(dna_strands) > 1:
        max_overlap = -1
        best_pair = (0, 0)
        best_merged = ""

        for i in range(len(dna_strands)):
            for j in range(len(dna_strands)):
                if i != j:
                    overlap_len = overlap_matrix[(i, j)]
                    merged = merge(dna_strands[i], dna_strands[j], overlap_len)
                    if overlap_len > max_overlap:
                        max_overlap = overlap_len
                        best_pair = (i, j)
                        best_merged = merged

        i, j = best_pair
        dna_strands[i] = best_merged
        del dna_strands[j]

        overlap_matrix = {}
        for k in range(len(dna_strands)):
            for l in range(len(dna_strands)):
                if k != l:
                    overlap_matrix[(k, l)] = overlap(dna_strands[k], dna_strands[l])

    return dna_strands[0]


def longest_common_subsequence(S1, S2):
    m = len(S1)
    n = len(S2)

    L = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S1[i - 1] == S2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    index = L[m][n]
    lcs = [""] * index

    i = m
    j = n
    while i > 0 and j > 0:
        if S1[i - 1] == S2[j - 1]:
            lcs[index - 1] = S1[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1


    return "".join(lcs)
