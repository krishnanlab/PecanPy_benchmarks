import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold as skf
from sklearn.linear_model import LogisticRegression as LogReg
from sklearn.metrics import roc_auc_score as auroc

def load_label(fp, min_size=10):
    """Load label from file and construct label matrix

    Notes:
        Orders of label not not the same as the original, labelsets might be 
        excluded due to few positive samples.        

    Args:
        fp(str): path to '.tsv' file for label, this file contains two columns, 
            first column is entity ID and second is label ID
        min_size(int): minimm size of labelset below which are discarded

    Returns:
        label_mat: numpy matrix, rows are entities and columns are labels
        IDmap(dict): dictionary for mapping entity ID to index

    """
    print("Loading label file from: %s"%fp)

    labelsets = {}
    with open(fp, 'r') as f:
        for line in f:
            ID, label = line.strip().split('\t')
            label = int(label)
            ID = int(ID)
            
            if label not in labelsets:
                labelsets[label] = []

            labelsets[label].append(ID)

    pop_lst = []
    for label, labelset in labelsets.items():
        if len(labelset) < 10:
            pop_lst.append(label)

    for label in pop_lst:
        labelsets.pop(label)

    IDs = set()
    for labelset in labelsets.values():
        IDs.update(labelset)

    IDmap = {j:i for i,j in enumerate(IDs)}

    n_nodes = len(IDmap)
    n_classes = len(labelsets)
    label_mat = np.zeros((n_nodes, n_classes), dtype=bool)
    
    for i, labelset in enumerate(labelsets.values()):
        for ID in labelset:
            label_mat[IDmap[ID], i] = True

    return label_mat, IDmap


def load_emb(fp):
    """Load embedding from `.emb` file

    Args:
        fp(str): path to `.emb` file

    Returns:
        emb: embedding vectors as numpy matrix
        IDmap: mapping from ID to corresponding index

    """
    print("Loading embedding file from: %s"%fp)
    emb = np.loadtxt(fp, delimiter=' ', skiprows=1)
    IDmap = {j:i for i,j in enumerate(emb[:,0].astype(int).tolist())}

    return emb[:,1:], IDmap


def test(emb, label_mat, emb_IDmap, label_IDmap, n_splits, random_state, shuffle):
    """Test embedding performance

     Perform node classification using L2 regularized Logistic Regression 
     with 5-Fold Cross Validation

    """
    n_classes = label_mat.shape[1]
    label_IDs = list(label_IDmap)
    emb_idx = [emb_IDmap[ID] for ID in label_IDs]
    x = emb[emb_idx]

    splitter = skf(n_splits=n_splits, random_state=random_state, shuffle=shuffle)
    mdl = LogReg(penalty='l2', solver='lbfgs', warm_start=False, max_iter=1000)

    y_true_all = []
    y_pred_all = []

    for i in range(n_classes):
        y = label_mat[:,i]
        label = i + 1

        y_true = np.array([], dtype=bool)
        y_pred = np.array([])

        for j, (train, test) in enumerate(splitter.split(y, y)):
            print("Testing class #{:>4d},\tfold {:>2d} / {:<2d}"
                  .format(label, j + 1, n_splits), flush=True, end='\r')
            mdl.fit(x[train], y[train])

            y_true = np.append(y_true, y[test])
            y_pred = np.append(y_pred, mdl.decision_function(x[test]))

        y_true_all.append(y_true)
        y_pred_all.append(y_pred)

    print('')

    return y_true_all, y_pred_all


def eval(emb, label_mat, emb_IDmap, label_IDmap, n_splits=5, random_state=None, shuffle=False):
    """Evaluate predictions using auROC

    Args:
        emb(:obj:`np.ndarray`): embedding matrix
        label_mat(:obj:`np.ndarray`): label matrix
        emb_IDmap(dict of `str`:`int`): IDmap for embedding matrix
        label_IDmap(dict of `str`:`int`): IDmap fro label matrix
        n_splits(int): number folds in stratified k-fold cross validation
        random_state(int): random state used to generate split

    """
    y_true_all, y_pred_all = test(emb, label_mat, emb_IDmap, label_IDmap,
                                  n_splits=n_splits, random_state=random_state,
                                  shuffle=shuffle)

    auroc_all = [auroc(y_true, y_pred) for y_true, y_pred in zip(y_true_all, y_pred_all)]

    return auroc_all

networks = ['BlogCatalog', 'PPI', 'Wikipedia'] # small graphs that have node labels for classification
methods_lst = os.popen("cat ../../data/implementation_list.txt").read().split()
emb_pth = '../../result/emb'
out_pth = '../../result/evaluation_summary.tsv'
n_iter = 10
n_splits = 5

result_df = pd.DataFrame()
for network in networks:
    label_mat, label_IDmap = load_label('../../data/labels/%s.tsv'%network)
    size = label_mat.shape[1]

    for method in methods_lst:
        df = pd.DataFrame()

        emb, emb_IDmap = load_emb('/'.join([emb_pth, method, network]) + '.emb')

        auroc_mat = None

        for i in range(n_iter):
            auroc_score = eval(emb, label_mat, emb_IDmap, label_IDmap, 
                         n_splits=n_splits, random_state=i, shuffle=True)

            if auroc_mat is None:
                auroc_mat = np.zeros((len(auroc_score), n_iter))

            auroc_mat[:,i] = auroc_score
            
        auroc_score = np.mean(auroc_mat, axis=1)

        df['auROC'] = auroc_score
        df['Network'] = network
        df['Method'] = method
        df['Index'] = list(range(size))

        result_df = pd.concat([result_df, df], sort=False)

        print("auROC: mean = %.4f, std =  %.4f, median = %.4f\n"%\
              (np.mean(auroc_score),  np.std(auroc_score), np.median(auroc_score)))

result_df.to_csv(out_pth, index=False, sep='\t')
