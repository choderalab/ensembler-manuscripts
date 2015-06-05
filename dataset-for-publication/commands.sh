#!/bin/bash

ensembler init
ensembler gather_targets --query 'family:"tyr protein kinase family" AND organism:"homo sapiens" AND reviewed:yes' --uniprot_domain '^Protein kinase(?!; truncated)(?!; inactive)'
ensembler gather_templates --gather_from uniprot --query 'domain:"Protein kinase" AND reviewed:yes' --uniprot_domain_regex '^Protein kinase(?!; truncated)(?!; inactive)'
ensembler loopmodel
ensembler align
ensembler build_models
ensembler cluster
ensembler refine_implicit
