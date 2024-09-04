import numpy as np
from sklearn.decomposition import PCA

def PCATransform(train_data, n_components, n_examples, img_size = 448):
    train_len, feat_num = train_data.shape

    pca = PCA(n_components=n_components, whiten=True)
    y = pca.fit_transform(train_data)
    k = int(n_examples / n_components)
    left_border = pca.mean_[:n_components] - 3 * pca.explained_variance_
    right_border = pca.mean_[:n_components] + 3 * pca.explained_variance_
    h = (right_border - left_border) / k
    step = np.eye(n_components) * h

    data = [[] for i in range(n_components)]
    for i in range(k):
        temp = left_border + i * step
        for j in range(n_components):
            data[j].append(temp[j])

    data = np.vstack([np.vstack(x) for x in data])


    transformed = pca.inverse_transform(data)
    if feat_num == 106:
        transformed = transformed.reshape((n_examples, 106))
    else:
        transformed = transformed.reshape((n_examples, 106, int(feat_num / 106)))

    return transformed