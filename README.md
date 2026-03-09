# 🚀 SEISMIC METAMATERIAL INVERSE DESIGN

## Machine Learning–Driven Design of Seismic Bandgap Structures

This project develops a machine learning framework for the inverse design of seismic metamaterials, combining COMSOL finite element simulations with deep neural networks to generate unit-cell structures with target seismic bandgaps.

---

# 📂 Project Structure

## 📊 Dataset Generation
Scripts for generating metamaterial topology datasets and extracting bandgap labels from COMSOL simulations.  
Unit cells are represented as 50×50 binary images with symmetry and filling constraints.

## 🧠 VAE for ML
A Variational Autoencoder (VAE) compresses high-dimensional metamaterial geometries into a low-dimensional latent space for efficient learning.

## ⚡ Inverse Design Model
A neural network searches the latent space to generate structures with target seismic bandgaps.  
The generated structures are reconstructed and verified with FEM simulations.

---

# 🛠 Tech Stack

- COMSOL Multiphysics  
- MATLAB  (COMSOL with MATLAB Livelink)
- Python  
- TensorFlow
