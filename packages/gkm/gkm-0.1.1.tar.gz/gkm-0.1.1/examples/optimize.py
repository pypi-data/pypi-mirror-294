import numpy as np
import matplotlib.pyplot as plt
import gkm


def fit_and_plot(x, y, lmbda, gamma, loss, ax):
    xsqr = (x ** 2).sum(axis=1)
    dsqr = xsqr[:, None] + xsqr[None, :] - 2.0 * x.dot(x.T)
    k = np.exp(-gamma * dsqr)

    clf = gkm.GKM(lmbda=lmbda, loss=loss)
    clf.fit_with_kernel_matrix(k, y)

    yp = clf.predict_with_kernel_matrix(k)
    ax.scatter(x[:, 0], x[:, 1], s=np.maximum(0.0, yp))


def main():
    # generate data
    np.random.seed(5)
    n, nft = 500, 3
    x = np.random.rand(n, nft)
    y = 50.0 * np.prod(np.sin(2.0 * np.pi * x[:, :2]), axis=1) ** 2

    # rescale features
    xsqr = (x ** 2).sum(axis=1)
    dsqr = xsqr[:, None] + xsqr[None, :] - 2.0 * x.dot(x.T)
    mscale = np.mean(dsqr)
    x /= np.sqrt(mscale)

    # optimize
    loss = gkm.deviance.poisson
    clf = gkm.OptimizedGKM(
        loss=loss,
        regularization=gkm.regularization.penalize_gamma(1e-6),
        lmbda0=1e-3,
        gamma0='auto',
        kernel_type='multi-rbf',
        verbose=1,
    )
    clf.fit(x, y)

    print('lmbda:', clf.lmbda0, '->', clf.lmbda)
    print('gamma:', clf.gamma0[0], '->', clf.gamma[0])
    print('value:', clf.value0, '->', clf.value)

    # visualize resulting decision functions
    fig, ax = plt.subplots(1, 3, figsize=(10, 4))
    fit_and_plot(x, y, clf.lmbda0, clf.gamma0[0], loss, ax[0])
    ax[0].set_title('initial predictions')
    fit_and_plot(x, y, clf.lmbda, clf.gamma[0], loss, ax[1])
    ax[1].set_title('final predictions')
    ax[2].scatter(x[:, 0], x[:, 1], s=y)
    ax[2].set_title('true labels')
    plt.show()


if __name__ == '__main__':
    main()
