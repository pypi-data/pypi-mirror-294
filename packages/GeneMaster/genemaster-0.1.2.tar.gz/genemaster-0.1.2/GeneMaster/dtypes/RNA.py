from GeneMaster.GeneMaster.operations.RNAOperations import rna_visualizations
from GeneMaster.GeneMaster.operations.RNAOperations import nucleotide_frequency
from GeneMaster.GeneMaster.operations.RNAOperations import dna_transcription
from GeneMaster.GeneMaster.operations.RNAOperations import compute_gc_content_rna
from GeneMaster.GeneMaster.operations.RNAOperations import protein_transcription
from GeneMaster.GeneMaster.operations.RNAOperations import most_frequent_kmer


class RNA:
    def __init__(self, sequence):
        valid_nucleotides = {'A', 'U', 'C', 'G'}
        if not all(nuc in valid_nucleotides for nuc in sequence.upper()):
            raise ValueError('Invalid RNA sequence')
        self.sequence = sequence.upper()
        self.length = len(self.sequence)
        self.frequency = nucleotide_frequency(self.sequence)
        self.visualize = rna_visualizations(self.sequence)
        self.A = self.sequence.count('A')
        self.U = self.sequence.count('U')
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
            return RNA(sub_sequence)
        elif isinstance(key, int):
            return RNA(self.sequence[key])
        else:
            raise TypeError("Invalid argument type.")

    def __contains__(self, item):
        if isinstance(item, RNA):
            item = str(item)
        elif not isinstance(item, str):
            raise TypeError("Item must be a string or RNA object")
        return item in self.sequence

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return RNA(self.sequence + other.sequence)
        return NotImplemented

    def __hash__(self):
        return hash(self.sequence)

    def transcribe_to_dna(self):
        from .DNA import DNA
        dna = dna_transcription(self.sequence)
        return DNA(dna)

    def gc_content(self):
        return compute_gc_content_rna(self.sequence)

    def translation(self):
        protein = ''.join(protein_transcription(self.sequence, steps=3))
        return protein

    def kmer(self, k):
        kmers = most_frequent_kmer(self.sequence, k)
        return kmers

