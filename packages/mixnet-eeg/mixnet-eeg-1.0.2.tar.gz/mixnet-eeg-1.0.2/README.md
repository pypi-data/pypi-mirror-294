<p align="center"> 
<img src="MixNet_overview_new.jpg" width="100%" height="100%"> 
</p>

### MixNet: Joining Force of Classical and Modern Approaches toward The Comprehensive Pipeline in Motor Imagery EEG Classification

Python API and the novel algorithm for motor imagery EEG recognition named MixNet. The API benefits BCI researchers ranging from beginners to experts. We demonstrate examples of using the API for loading benchmark datasets, preprocessing, training, and validating SOTA models, including MixNet. In summary, the API allows the researchers to construct the pipeline to benchmark the newly proposed models and very recently developed SOTA models.
  
---

## Getting started

### Dependencies

- Python==3.8.10
- tensorflow-gpu==2.7.0
- tensorflow-addons==0.16.1
- scikit-learn>=1.2.2
- wget>=3.2
- h5py==3.5.0
- pandas>=2.0

1. Create `conda`  environment with dependencies
```bash
wget https://github.com/Max-Phairot-A/MixNet/blob/main/environment.yml
conda env create -f environment.yml
conda activate mixnet
```

### Installation:

1. Using pip

  ```bash
  pip install mixnet-eeg
  ```
<!-- 2. Using the released python wheel

  ```bash
  wget https://github.com/IoBT-VISTEC/MIN2Net/releases/download/v1.0.0/min2net-1.0.0-py3-none-any.whl
  pip install min2net-1.0.0-py3-none-any.whl
  ``` -->

### Citation

To read & cite [our paper](https://ieeexplore.ieee.org/document/10533256)

P. Autthasan, R. Chaisaen, H. Phan, M. D. Vos and T. Wilaiprasitporn, "MixNet: Joining Force of Classical and Modern Approaches toward The Comprehensive Pipeline in Motor Imagery EEG Classification," in IEEE Internet of Things Journal, doi: 10.1109/JIOT.2024.3402254.

```
@ARTICLE{10533256,
  author={Autthasan, Phairot and Chaisaen, Rattanaphon and Phan, Huy and Vos, Maarten De and Wilaiprasitporn, Theerawit},
  journal={IEEE Internet of Things Journal}, 
  title={MixNet: Joining Force of Classical and Modern Approaches Toward the Comprehensive Pipeline in Motor Imagery EEG Classification}, 
  year={2024},
  volume={11},
  number={17},
  pages={28539-28554},
  keywords={Electroencephalography;Task analysis;Feature extraction;Measurement;Internet of Things;Multitasking;Motors;Adaptive gradient blending;brain-computer interface (BCI);deep learning (DL);motor imagery (MI);multitask learning},
  doi={10.1109/JIOT.2024.3402254}}
```

### License
Copyright &copy; 2021-All rights reserved by [INTERFACES (BRAIN lab @ IST, VISTEC, Thailand)](https://www.facebook.com/interfaces.brainvistec).
Distributed by an [Apache License 2.0](https://github.com/Max-Phairot-A/MixNet/blob/main/LICENSE).
