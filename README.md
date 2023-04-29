# SVD Image Compression

## Singular Value Decomposition

Singular Value Decomposition (SVD) states that every (m×n)‑matrix A can be written as a product

$A = U \cdot \Sigma \cdot V^T$

where $U$ and $V$ are orthogonal matrices and the the matrix $\Sigma$ consists of descending non-negative values on its diagonal and zeros elsewhere. The entries $σ1 ≥ σ2 ≥ σ3 ≥ … ≥ 0$ on the diagonal of $\Sigma$ are called the singular values of A. Geometrically, $\Sigma$ maps the j‑th unit coordinate vector of n‑dimensional space to the j‑th coordinate vector of m‑dimensional space, scaled by the factor $σ_j$. Orthogonality of $U$ and $V$ means that they correspond to rotations of m‑dimensional and n‑dimensional space, respectively. Therefore, only $\Sigma$ changes the length of vectors.