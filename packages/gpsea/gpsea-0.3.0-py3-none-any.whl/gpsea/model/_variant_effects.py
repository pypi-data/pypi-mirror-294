from enum import Enum


class VariantEffect(Enum):
    """
    `VariantEffect` represents consequences of a variant on transcript that are supported by GPSEA.

    .. doctest::

      >>> from gpsea.model import VariantEffect
      >>> missense = VariantEffect.MISSENSE_VARIANT
      >>> print(missense)
      missense_variant

    The `VariantEffect` has a :attr:`curie` attribute that represents the ontology class from
    `Sequence Ontology <http://www.sequenceontology.org/>`_.

    .. doctest::

      >>> missense.curie
      'SO:0001583'
    """

    TRANSCRIPT_ABLATION = "SO:0001893"
    SPLICE_ACCEPTOR_VARIANT = "SO:0001574"
    SPLICE_DONOR_VARIANT = "SO:0001575"
    STOP_GAINED = "SO:0001587"
    FRAMESHIFT_VARIANT = "SO:0001589"
    STOP_LOST = "SO:0001578"
    START_LOST = "SO:0002012"
    TRANSCRIPT_AMPLIFICATION = "SO:0001889"
    INFRAME_INSERTION = "SO:0001821"
    INFRAME_DELETION = "SO:0001822"
    MISSENSE_VARIANT = "SO:0001583"
    PROTEIN_ALTERING_VARIANT = "SO:0001818"
    SPLICE_REGION_VARIANT = "SO:0001630"
    SPLICE_DONOR_5TH_BASE_VARIANT = "SO:0001787"
    SPLICE_DONOR_REGION_VARIANT = "SO:0002170"
    SPLICE_POLYPYRIMIDINE_TRACT_VARIANT = "SO:0002169"
    INCOMPLETE_TERMINAL_CODON_VARIANT = "SO:0001626"
    START_RETAINED_VARIANT = "SO:0002019"
    STOP_RETAINED_VARIANT = "SO:0001567"
    SYNONYMOUS_VARIANT = "SO:0001819"
    CODING_SEQUENCE_VARIANT = "SO:0001580"
    MATURE_MIRNA_VARIANT = "SO:0001620"
    FIVE_PRIME_UTR_VARIANT = "SO:0001623"
    THREE_PRIME_UTR_VARIANT = "SO:0001624"
    NON_CODING_TRANSCRIPT_EXON_VARIANT = "SO:0001792"
    INTRON_VARIANT = "SO:0001627"
    NMD_TRANSCRIPT_VARIANT = "SO:0001621",
    NON_CODING_TRANSCRIPT_VARIANT = "SO:0001619"
    UPSTREAM_GENE_VARIANT = "SO:0001631"
    DOWNSTREAM_GENE_VARIANT = "SO:0001632"
    TFBS_ABLATION = "SO:0001895"
    TFBS_AMPLIFICATION = "SO:0001892"
    TF_BINDING_SITE_VARIANT = "SO:0001782"
    REGULATORY_REGION_ABLATION = "SO:0001894"
    REGULATORY_REGION_AMPLIFICATION = "SO:0001891"
    FEATURE_ELONGATION = "SO:0001907"
    REGULATORY_REGION_VARIANT = "SO:0001566"
    FEATURE_TRUNCATION = "SO:0001906"
    INTERGENIC_VARIANT = "SO:0001628"
    SEQUENCE_VARIANT = "SO:0001060"

    def __init__(self, curie: str):
        self._curie = curie

    @property
    def curie(self) -> str:
        """
        Get a compact URI (CURIE) of the variant effect
        (e.g. `SO:0001583` for a missense variant).
        """
        return self._curie

    def __str__(self) -> str:
        return self.name.lower()
