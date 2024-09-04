# tests/test_dna.py
import unittest
from myPackage import DNA
from myPackage import RNA


class TestDNA(unittest.TestCase):
    def test_reverse_complement(self):
        dna_seq = DNA("ATGCGT")
        self.assertEqual(dna_seq.revComplement(), DNA("ACGCAT"))

    def test_gc_content(self):
        dna_seq = DNA("ATGCGT")
        self.assertAlmostEqual(dna_seq.gc_content(), 0.5)

    def test_transcription(self):
        dna_seq = DNA("ATGCGT")
        rna_seq = dna_seq.transcribe_to_rna()
        self.assertEqual(rna_seq, RNA("ACGCAU"))

    def test_start_stop_codons(self):
        dna_seq = DNA("ATGATGTAGTAATGA")
        positions = dna_seq.start_stop_codons(overlap=False)
        self.assertEqual(positions, [(0, 9)])

    def test_orf(self):
        dna_seq = DNA(
            "AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG")
        result = dna_seq.find_orf()
        correct_ans = ['MLLGSFRLIPKETLIQVAGSSPCNLS-', 'M-', 'MGMTPRLGLESLLE-', 'MTPRLGLESLLE-']
        self.assertEqual(sorted(result), sorted(correct_ans))

    def test_arith(self):
        dna_seq = DNA("ATGC")
        test = DNA("ATGA")
        self.assertEqual(dna_seq < test, False)
        self.assertEqual(dna_seq > test, True)
        self.assertEqual(dna_seq <= test, False)
        self.assertEqual(dna_seq >= test, True)
        self.assertEqual(dna_seq == test, False)
        self.assertEqual(dna_seq != test, True)

    def test_exons(self):
        dna_seq = DNA('ATGCGTACGTAGCCTGAAGCTAGGC')
        result = dna_seq.extract_exons()
        correct = DNA('ATGCGTACGTAG')
        self.assertEqual(result, correct)

    def test_introns(self):
        dna_seq = DNA('ATGCGTACGTAGCCTGAAGCTAGGC')
        result = dna_seq.extract_introns()
        correct = DNA('CCTGAAGCTAGGC')
        self.assertEqual(result, correct)

    def test_melting_temp(self):
        dna_seq = DNA('ATGCGTACGTAGCCTGAAGCTAGGC')
        result = dna_seq.melting_temperature()
        correct = 61
        self.assertEqual(round(result, 0), correct)

    def test_translation(self):
        dna_seq = DNA('ATGCGTACGTAGCCT')
        result = dna_seq.translation()
        correct = 'MRT-P'
        self.assertEqual(result, correct)

    def test_kmer(self):
        dna_seq = DNA('ATGCGATGC')
        result = dna_seq.kmer(3)
        correct = {'ATG': 2, 'TGC': 2, 'GCG': 1, 'CGA': 1, 'GAT': 1}
        self.assertEqual(result, correct)


if __name__ == '__main__':
    unittest.main()
