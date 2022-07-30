from django.db import models

# Create your models here.


class ID_Mapper(models.Model):
    """ id_mapper_xxx.txt schema"""
    ek_gene_id = models.BigIntegerField(verbose_name='EK_GENE_ID', primary_key=True)
    gene_id = models.CharField(verbose_name='ensembl gene id', max_length=20)
    source = models.IntegerField(verbose_name='binary representation of availablity - ens+entrez+vgnc')
    entrez_id = models.BigIntegerField(verbose_name='entrez gene id', null=True)
    vgnc_id = models.CharField(verbose_name='vgnc id', max_length=20, null=True)
    vgnc_symbol = models.CharField(verbose_name='vgnc symbol', max_length=30, null=True)
    hgnc_orthologs = models.CharField(verbose_name='hgnc orthologs id', max_length=20, null=True)
    human_gene_id = models.CharField(verbose_name='human ensembl gene id', max_length=20, null=True)
    human_entrez_id = models.BigIntegerField(verbose_name='human gene entrez identifier', null=True)
    hgnc_symbol = models.CharField(verbose_name='hgnc human orthologs gene symbol', max_length=20, null=True)

    class Meta:
        ordering = ['ek_gene_id']

    def __str__(self) -> str:
        return self.gene_id


class Gene(models.Model):
    """  genes_xxd.txt schema """
    ek_gene = models.ForeignKey(to='ID_Mapper', to_field='ek_gene_id', on_delete=models.CASCADE, default=-1)
    seqname = models.CharField(verbose_name='chromosome', max_length=5)
    start = models.IntegerField(verbose_name='gene start coordinates')
    end = models.IntegerField(verbose_name='gene end coordinates')
    gene_biotype = models.CharField(verbose_name='gene biotype', max_length=50)
    strand = models.CharField(verbose_name='strand', max_length=1)

    class Meta:
        indexes = [models.Index(fields=['seqname', 'start', 'end'])]
        ordering = ['ek_gene']

    def __str__(self) -> str:
        return str(self.ek_gene)


class Exon(models.Model):
    """ exons_xxx.txt schema"""
    ek_gene = models.ForeignKey(to='ID_Mapper', to_field='ek_gene_id', on_delete=models.CASCADE, default=-1)
    exon_id = models.CharField(verbose_name='ensembl exon id', max_length=20)
    start = models.IntegerField(verbose_name='exon start coordinates')
    end = models.IntegerField(verbose_name='exon end coordinates')
    gene_biotype = models.CharField(verbose_name='gene biotype', max_length=50)
    strand = models.CharField(verbose_name='strand', max_length=1)
    transcript_id = models.TextField(verbose_name='corresponding ens transcript id')

    class Meta:
        ordering = ['ek_gene']

    def __str__(self) -> str:
        return self.exon_id


class ComputedFeatures(models.Model):
    """  computed_feature_xxx.csv schema"""
    ek_gene = models.ForeignKey(to='ID_Mapper', to_field='ek_gene_id', on_delete=models.CASCADE, default=-1)
    feature = models.CharField(max_length=25)
    start = models.IntegerField(verbose_name='current computed feature start coordinates')
    end = models.IntegerField(verbose_name='current computed feature end coordinates')

    class Meta:
        ordering = ['ek_gene']

    def __str__(self) -> str:
        return str(self.ek_gene) + ': ' + self.feature + ' ' + str(self.start) + ' - ' + str(self.end)


class Feature(models.Model):
    """ features_xxx.txt schema"""
    ek_gene = models.ForeignKey(to='ID_Mapper', to_field='ek_gene_id', on_delete=models.CASCADE, default=-1)
    feature = models.CharField(verbose_name='feature annotation in gtf', max_length=16)
    start = models.IntegerField(verbose_name='feature start coordinates')
    end = models.IntegerField(verbose_name='feature end coordinates')
    gene_biotype = models.CharField(verbose_name='gene biotype', max_length=50)
    strand = models.CharField(verbose_name='strand', max_length=1)

    class Meta:
        ordering = ['ek_gene']

    def __str__(self) -> str:
        return str(self.ek_gene) + ' - ' + self.feature


class Pathway_Meta(models.Model):
    """ pathway_meta_xxx.txt schema """
    pathway_meta_id = models.IntegerField(verbose_name='database unit meta_data id', primary_key=True)
    species = models.CharField(verbose_name='current species', max_length=10)
    name = models.CharField(verbose_name='current db unit name', max_length=20)
    id_type = models.CharField(verbose_name='the id type of the current db unit', max_length=50)
    update_time = models.CharField(verbose_name='current db unit update time', max_length=20)

    def __str__(self) -> str:
        return self.name


class Pathway(models.Model):
    """  pathways_xxx.txt schema"""
    ek_pathway_id = models.BigIntegerField(verbose_name='EK_PATHWAY_ID', primary_key=True)
    pathway_id = models.CharField(verbose_name='pathway id in corresponding db', max_length=20)
    pathway_description = models.TextField()
    pathway_meta = models.ForeignKey(to='Pathway_Meta', to_field='pathway_meta_id', on_delete=models.CASCADE, default=-1)

    class Meta:
        ordering = ['ek_pathway_id']

    def __str__(self) -> str:
        return self.pathway_id


class Involve(models.Model):
    """ involve_xxx.txt  schema"""
    ek_gene = models.ForeignKey(to='ID_Mapper', to_field='ek_gene_id', on_delete=models.CASCADE, default=-1)
    ek_pathway = models.ForeignKey(to='Pathway', to_field='ek_pathway_id', on_delete=models.CASCADE, default=-1)

    def __str__(self) -> str:
        return str(self.ek_gene) + ' - ' + str(self.ek_pathway)
