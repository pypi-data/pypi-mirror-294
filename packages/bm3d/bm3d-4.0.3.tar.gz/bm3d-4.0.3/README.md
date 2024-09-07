# Python wrapper for BM3D denoising - from Tampere with love

Python wrapper for BM3D for stationary correlated noise (including white noise) for color,
grayscale and multichannel images and deblurring.

BM3D is an algorithm for attenuation of additive spatially correlated
stationary (aka colored) Gaussian noise. This package provides a wrapper
for the BM3D binaries for use for grayscale, color and other multichannel images
for denoising and deblurring.

This implementation is based on
- Y. Mäkinen, L. Azzari, A. Foi, 2020, "Collaborative Filtering of Correlated Noise: Exact Transform-Domain Variance
for Improved Shrinkage and Patch Matching", in IEEE Transactions on Image Processing, vol. 29, pp. 8339-8354.
- K. Dabov, A. Foi, V. Katkovnik, K. Egiazarian, 2007, "Image Denoising by Sparse 3-D Transform-Domain Collaborative
Filtering", in IEEE Transactions on Image Processing, vol. 16, pp. 2080-2095.

This package provides a BM3D interface for the "bm4d" denoising package. Please see the 
[bm4d](https://pypi.org/project/bm4d) package for supported platforms.

The package is available for non-commercial use only. For details, see LICENSE.

For examples, see the examples folder of the full source (bm3d-***.tar.gz) from https://pypi.org/project/bm3d/#files , 
which also includes the example noise cases demonstrated in the paper.

Authors: \
    Ymir Mäkinen <ymir.makinen@tuni.fi> \
    Lucio Azzari \
    Alessandro Foi



