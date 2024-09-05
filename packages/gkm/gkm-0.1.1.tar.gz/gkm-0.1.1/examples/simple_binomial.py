import numpy as np
import matplotlib.pyplot as plt
import gkm


def main():
    np.random.seed(5)
    n, nft = 1000, 2
    x = np.random.rand(n, nft)
    y = 5.0 * np.prod(np.sin(2.0 * np.pi * x), axis=1) ** 2
    y = np.round(y)

    xsqr = (x ** 2).sum(axis=1)
    dsqr = xsqr[:, None] + xsqr[None, :] - 2.0 * x.dot(x.T)
    mscale = np.mean(dsqr)
    x /= np.sqrt(mscale)

    clf = gkm.GKM(lmbda=1e-6, loss=gkm.deviance.Binomial(5), verbose=2)
    clf.fit(x, y)

    f = clf.predict(x)
    print(np.hstack((y[:, None], np.floor(f[:, None]))))

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].scatter(x[:, 0], x[:, 1], s=y)
    ax[1].scatter(x[:, 0], x[:, 1], s=np.maximum(0.0, f))
    plt.show()


if __name__ == '__main__':
    main()
