# SVD Image Compression

## Setup

The `requirements.txt` file should list all Python libraries that `SVD.py` depends on, and they can be installed using:

```
pip install -r requirements.txt
```

## Singular Value Decomposition

Singular Value Decomposition (SVD) states that every (m×n)‑matrix $A$ can be written as a product

$A = U \cdot \Sigma \cdot V^T$

where $U$ and $V$ are orthogonal matrices and the the matrix $\Sigma$ consists of descending non-negative values on its diagonal and zeros elsewhere. The entries $σ_1 ≥ σ_2 ≥ σ_3 ≥ … ≥ 0$ on the diagonal of $\Sigma$ are called the singular values of A. Geometrically, $\Sigma$ maps the j‑th unit coordinate vector of n‑dimensional space to the j‑th coordinate vector of m‑dimensional space, scaled by the factor $σ_j$. Orthogonality of $U$ and $V$ means that they correspond to rotations of m‑dimensional and n‑dimensional space, respectively. Therefore, only $\Sigma$ changes the length of vectors.

## Image Compression

In this instance, a given PNG image can be broken down into three channels: red, green, and blue. Each channel can be represented as a (m×n)-matrix with values ranging from 0 to 255. For more information on the RGB color model, press [here](https://en.wikipedia.org/wiki/RGB_color_model). Since, $σ_1 ≥ σ_2 ≥ σ_3 ≥ … ≥ 0$, the data in the matrices $U, \Sigma, V^T$ is sorted by how much it contributes to the matrix $A$ in the product. For a number $n$ of singular values, we take the first $k$ columns of $U$ and $V$ and the upper left (nxn)-square of $\Sigma$, containing the $n$ largest singular values. Although there are [better methods for image compression](https://en.wikipedia.org/wiki/JPEG), this was a fun project to write from scratch using my linear algebra and CS knowledge. 

## Energy

Where a number $n$ of singular values and a number $k$ is the rank of the input matrix, the energy for a given channel is given by

$E = \frac{\Sigma_{i=1}^{n} {σ_i}^2}{\Sigma_{i=1}^{k} {σ_i}^2}$

## Output

In the `images` folder, three example images can be found that the user can compress (or not, up to you). `car.png`'s compression looks as follows with a number $n$ of singular values equal to $20$:

![`car.png`](https://i.imgur.com/TnOybsG.png "car.png")

Please feel free to work on the present issue or expand on the project. Special thanks to Professor Mikucki and [Tim Baumann](http://timbaumann.info/svd-image-compression-demo/).