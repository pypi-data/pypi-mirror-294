from GeneMaster.operations.DNAOperations import reverse_complement
from GeneMaster.operations.DNAOperations import compute_gc_content
from GeneMaster.operations.DNAOperations import rna_transcription
from GeneMaster.operations.DNAOperations import define_start_stop_codons
from GeneMaster.operations.DNAOperations import open_reading_frames
from GeneMaster.operations.DNAOperations import nucleotide_frequency
from GeneMaster.operations.DNAOperations import extract_exon_parts
from GeneMaster.operations.DNAOperations import extract_intron_parts
from GeneMaster.operations.DNAOperations import find_motif_sequence
from GeneMaster.operations.DNAOperations import compute_melting_temperature
from GeneMaster.operations.DNAOperations import dna_visualization
from GeneMaster.operations.DNAOperations import make_pairwise_align
from GeneMaster.operations.DNAOperations import compute_codon_bias
from GeneMaster.operations.DNAOperations import protein_transcription
from GeneMaster.operations.DNAOperations import most_frequent_kmer


class DNA:
    def __init__(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        if not all(nuc in valid_nucleotides for nuc in sequence.upper()):
            raise ValueError('Invalid DNA sequence')
        self.sequence = sequence.upper()
        self.length = len(self.sequence)
        self.complement = reverse_complement(self.sequence)
        self.frequency = nucleotide_frequency(self.sequence)
        self.visualize = dna_visualization(self.sequence)
        self.A = self.sequence.count('A')
        self.T = self.sequence.count('T')
        self.C = self.sequence.count('C')
        self.G = self.sequence.count('G')

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return self.sequence

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.sequence == other.sequence
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.sequence < other.sequence
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.sequence <= other.sequence
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.sequence > other.sequence
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.sequence >= other.sequence
        return NotImplemented

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self.sequence)
            step = key.step if key.step is not None else 1
            sub_sequence = self.sequence[start:stop:step]
            return DNA(sub_sequence)
        elif isinstance(key, int):
            return DNA(self.sequence[key])
        else:
            raise TypeError("Invalid argument type.")

    def __contains__(self, item):
        if isinstance(item, DNA):
            item = str(item)
        elif not isinstance(item, str):
            raise TypeError("Item must be a string or DNA object")
        return item in self.sequence

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return DNA(self.sequence + other.sequence)
        return NotImplemented

    def __hash__(self):
        return hash(self.sequence)

    def revComplement(self):
        result = reverse_complement(self.sequence)
        return DNA(result)

    def gc_content(self):
        return compute_gc_content(self.sequence)

    def transcribe_to_rna(self):
        from .RNA import RNA

        rna_seq = rna_transcription(self.sequence)
        return RNA(rna_seq)

    def start_stop_codons(self, overlap=True):
        positions = define_start_stop_codons(self.sequence, self.length, overlap)
        return positions

    def find_orf(self):
        orf_prot = open_reading_frames(self.sequence)
        return orf_prot

    def extract_exons(self):
        exon_pos = define_start_stop_codons(self.sequence, self.length, overlap=True)
        exons = extract_exon_parts(self.sequence, exon_pos)
        return DNA(exons)

    def extract_introns(self):
        exon_pos = define_start_stop_codons(self.sequence, self.length, overlap=False)
        introns = extract_intron_parts(self.sequence, exon_pos)
        return DNA(introns)

    def find_motif(self, motif):
        motif_pos = find_motif_sequence(self.sequence, motif)
        return motif_pos

    def melting_temperature(self):
        temp = compute_melting_temperature(self.sequence, self.length)
        return temp

    def pairwise_align(self, seq):
        aligned_seq_1, aligned_seq_2 = make_pairwise_align(self.sequence, str(seq))
        return aligned_seq_1, aligned_seq_2

    def codon_bias(self):
        bias = compute_codon_bias(self.sequence)
        return bias

    def translation(self):
        protein = ''.join(protein_transcription(self.sequence, steps=3))
        return protein

    def kmer(self, k):
        kmers = most_frequent_kmer(self.sequence, k)
        return kmers
