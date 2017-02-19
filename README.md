# DLS-Singapore
NUS hackathon

## Things to read
1. https://www.blackhat.com/docs/us-16/materials/us-16-Berlin-An-AI-Approach-To-Malware-Similarity-Analysis-Mapping-The-Malware-Genome-With-A-Deep-Neural-Network.pdf
2. https://arxiv.org/pdf/1508.03096v2.pdf
3. Any tutorial on Auto-Encoders
 a. https://keras.io/getting-started/sequential-model-guide/
 b. 

## Dataset
1. Malware Files: https://drive.google.com/open?id=0B9fG_FJRJKS_d1BOUjJRZ2pWZEE
2. Reports on Malware Files: https://drive.google.com/file/d/0B9fG_FJRJKS_ZkxxT1BlbWh6MEU/view?usp=sharing
3. Benign Files: https://drive.google.com/open?id=0B9fG_FJRJKS_RnF5Ynhmb0R3WTQ
4. https://zeltser.com/malware-sample-sources/
5. https://www.kaggle.com/c/malware-classification/data


## Useful papers & info
### Malware representation
#### Execution Graph as vector
- Code Graph for Malware Detection: http://ieeexplore.ieee.org/document/4472801/
- BitBlaze Binary analysis platform: http://bitblaze.cs.berkeley.edu/
- HI-CFG: Construction by Binary Analysis and Application to Attack Polymorphism: https://people.eecs.berkeley.edu/~dawnsong/papers/hicfg.pdf
#### Binary sequence to vector
- we consider binaries of different length as a LSTM case, and turn it into a vector
- http://datascience.stackexchange.com/questions/6866/denoising-autoenoders-with-variable-length-input
- https://keras.io/getting-started/sequential-model-guide/
- https://www.reddit.com/r/MachineLearning/comments/3iidv2/is_it_a_good_idea_generate_sentence_vectors_using/

