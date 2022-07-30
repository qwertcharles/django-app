# from xml.parsers.expat import model
from django.contrib import admin
from . import models

# Register your models here.

from .models import ID_Mapper


@admin.register(models.ID_Mapper)
class ID_MapperAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['gene_id']


@admin.register(models.Gene)
class GeneAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = [
        'ek_gene',
        'seqname',
    ]
    # search_fields = ['ek_gene_id__icontains']  # ?
    search_fields = ['ID_Mapper__gene_id']  # ?


@admin.register(models.Exon)
class ExonAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['exon_id']


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['ek_gene']


@admin.register(models.Pathway_Meta)
class Pathway_MetaAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['name']


@admin.register(models.ComputedFeatures)
class ComputedFeaturesAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['ek_gene']


@admin.register(models.Pathway)
class PathwayAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        'pathway_id',
        'pathway_meta_id'
    ]
    search_fields = ['pathway_id']


@admin.register(models.Involve)
class InvolveAdmin(admin.ModelAdmin):
    list_per_page = 20
