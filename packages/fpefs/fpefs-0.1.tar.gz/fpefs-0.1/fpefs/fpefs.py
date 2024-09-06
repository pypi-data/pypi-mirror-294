import pandas as pd

def fpefs(data):
    """
    Feature Probability Estimation and Feature Selection.
    
    Parameters:
    data (pd.DataFrame): A pandas DataFrame containing the dataset with features and labels.
    
    Returns:
    pd.DataFrame: A DataFrame with the feature names and their estimated probabilities.
    """
    df = pd.DataFrame(data)
    col = len(df.columns)
    nfeatures = col - 1
    del df  # release memory
    X = data.iloc[:, 0:nfeatures]  
    y = data.iloc[:, -1]
    
    # Normalization
    X = round(((X - X.min()) / (X.max() - X.min())), 2)
    
    def unique(list1):
        """Return unique elements of a list."""
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list
    
    label = unique(y)
    numberOfLabel = len(label)
    Prob = []
    
    # Loop over features
    for j in range(nfeatures):
        ulist = unique(X.iloc[:, j])
        sizeulist = len(ulist)
        mu = 0
        ncount = 0
        for m in range(sizeulist):
            mlist = []
            for i in range(len(X)):
                if ulist[m] == X.iloc[i, j] and y[i] not in mlist:
                    mlist.append(y[i])
                if numberOfLabel == len(mlist):
                    break
            nc = len(mlist)
            if nc < numberOfLabel:
                mu += float(nc) / numberOfLabel
                ncount += 1
        
        if ncount == 0:
            Pvalue = 0
        else:
            Pvalue = round(1 - (0.5 * ((float(sizeulist - ncount) / sizeulist) + (float(mu) / ncount))), 2)
        
        Prob.append(Pvalue)
    
    Prob = pd.Series(Prob)
    dfcolumns = pd.DataFrame(X.columns)
    estimatedProbability = pd.concat([dfcolumns, Prob], axis=1)
    return estimatedProbability
