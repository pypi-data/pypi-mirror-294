import pkg_resources
import os
import pandas as pd
import anndata 
from scipy.sparse import csr_matrix

def load_CCLE(Dir = 'data'):
    
    print('Loading CCLE data .. ', end='')
    if len(Dir) > 0: Dir = Dir + '/'
    df_exp = pd.read_csv(Dir + 'CCLE_cellline_gene_exp.csv', index_col = 0)
    df_pd = pd.read_csv(Dir + 'CCLE_cellline_info.csv', index_col = 0)
    df_auc = pd.read_csv(Dir + 'CCLE_drug_response_auc.csv', index_col = 0)
    df_ec50 = pd.read_csv(Dir + 'CCLE_drug_response_ec50.csv', index_col = 0)
    df_drug_info = pd.read_csv(Dir + 'CCLE_drug_info.csv', index_col = 0)
    print('done')

    return df_exp, df_pd, df_auc, df_ec50, df_drug_info
    
    
def load_data( dataset = None ):

    data_folder = pkg_resources.resource_filename('mlbi', 'data')
    dlst = ['scores', 'time-series', 'time-series2', 'tcga-brca', 
            'metabric', 'cancerseek', 'ccle-ctrpv2']
    
    if dataset == 'scores':
        df = pd.read_csv( data_folder + '/scores.csv' )
        return df
        
    elif dataset == 'time-series':
        df = pd.read_csv( data_folder + '/Time_series.csv' )
        return df
        
    elif dataset == 'time-series2':
        df = pd.read_csv( data_folder + '/Time_series_rev.csv' )
        return df
        
    elif dataset == 'metabric':
        print('Loading METABRIC data .. ', end='')
        file = '/metabric_data_expression_median.csv'
        df_gep = pd.read_csv(data_folder + file, index_col=0).transpose().iloc[1:]
        file = '/metabric_clinical_data_used.csv'
        df_clinical = pd.read_csv(data_folder + file, index_col=0)

        idx2 = list(df_clinical.index.values)
        idx3 = []
        for i in idx2:
            s = i.replace('.', '-')
            idx3.append(s)
        
        rend = dict(zip(idx2, idx3))
        df_clinical.rename(index = rend, inplace = True)
        
        idx1 = list(df_gep.index.values)
        idx2 = list(df_clinical.index.values)
        idxc = list(set(idx1).intersection(idx2))

        df_gep = df_gep.loc[idxc,:]
        df_clinical = df_clinical.loc[idxc,:]
        print('done')
        
        return { 'gene_expression':  df_gep, 'clinical_info': df_clinical }

    elif dataset == 'tcga-brca':
        print('Loading TCGA-BRCA data .. ', end='')
        file = '/TCGA_BRCA_gene_exp.csv'
        df_gep = pd.read_csv(data_folder + file, index_col=0)
        file = '/TCGA_BRCA_clinical_info.csv'
        df_clinical = pd.read_csv(data_folder + file, index_col=0)
        print('done')
        
        return { 'gene_expression':  df_gep, 'clinical_info': df_clinical }

    elif dataset == 'cancerseek':
        file = '/CancerSEEK_protein.csv'
        df_gep = pd.read_csv(data_folder + file, index_col=0)
        file = '/CancerSEEK_clinical_info.csv'
        df_clinical = pd.read_csv(data_folder + file, index_col=0)

        return { 'protein_expression':  df_gep, 'clinical_info': df_clinical }
   
    elif dataset == 'ccle-ctrpv2':
        df_gep, df_pd, df_auc, df_ec50, df_drug_info = load_CCLE(Dir = data_folder)

        return { 'gene_expression':  df_gep, 'cellline_info': df_pd,
                 'auc':  df_auc, 'ec50': df_ec50, 'drug_info': df_drug_info}
   
    else:
        if dataset is not None:
            print('%s dataset not found.' % dataset)
        print('You can select one of .', dlst )
            
        return None


def load_anndata( dataset = None ):

    data = load_data(dataset)
    if dataset == 'metabric':
        genes = data['gene_expression'].columns.values.tolist()
        df_var = pd.DataFrame( {'gene': genes}, index = genes )
        adata = anndata.AnnData( X = csr_matrix(data['gene_expression']), obs = data['clinical_info'], var = df_var )
        return adata

    elif dataset == 'tcga-brca':
        genes = data['gene_expression'].columns.values.tolist()
        df_var = pd.DataFrame( {'gene': genes}, index = genes )
        adata = anndata.AnnData( X = csr_matrix(data['gene_expression']), obs = data['clinical_info'], var = df_var )
        return adata

    elif dataset == 'cancerseek':
        genes = data['protein_expression'].columns.values.tolist()
        df_var = pd.DataFrame( {'gene': genes}, index = genes )
        adata = anndata.AnnData( X = csr_matrix(data['protein_expression']), obs = data['clinical_info'], var = df_var )
        return adata

   
    elif dataset == 'ccle-ctrpv2':
        genes = data['gene_expression'].columns.values.tolist()
        df_var = pd.DataFrame( {'gene': genes}, index = genes )
        adata = anndata.AnnData( X = csr_matrix(data['gene_expression']), obs = data['cellline_info'], var = df_var )
        adata.obsm['auc'] = data['auc']
        adata.obsm['ec50'] = data['ec50']
        adata.uns['drug_info'] = data['drug_info']
        return adata
   
    else:
        return data

