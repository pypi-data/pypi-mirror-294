import numpy as np
import matplotlib.pyplot as plt
import gkm


def main():
    np.random.seed(5)
    n, nft = 1000, 2
    x = np.random.rand(n, nft)
    beta = 100 * np.random.rand(nft)
    t = x.dot(beta)
    # sigma = 0.1
    # y = t + sigma * np.random.randn(n)
    y = np.random.poisson(t, size=n)

    clf = gkm.GLM(loss=gkm.deviance.poisson, verbose=2)
    clf.fit(x, y)
    f = clf.predict(x)

    print(beta)
    print(clf.coeffs)

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].scatter(x[:, 0], x[:, 1], s=y)
    ax[1].scatter(x[:, 0], x[:, 1], s=np.maximum(0.0, f))
    plt.show()


if __name__ == '__main__':
    main()
