# Skin mole classifier | ISIC-Archive Reader
_A Convolutional Deep Neural Network with Adam Optimization and User-facing UI_
_by Philipp Bechhaus in association with deeplearning.ai, Stanford University and the ISIC® Archive_

# Usage
Use methods within the _dnn_utils.py_ and _prep_utils.py_ (has main method) files to customize own DNN with annotated skin mole images. Those include:
### prep_utils
> * Get Image UUIDs
> * Get JSON URLs
> * Get Image Download URLs
> * Get Diagnoses and corresponding UUIDs
> * Store images locally

### dnn_utils
> * Sigmoid activation
> * ReLu activation
> * Leaky ReLu activation
> * Forward propagation (2/n-layered)
> * backward propagation (2/n-layered)
> * Xavier initialization
> * He initialization
> * Cross-entropy cost calculation
> * Predict error method
> * Show mislabeled method


For quick API/images access, run _prep_utils.py_ from your Terminal of choice. The brief wizard will walk you through then.

Questions to _philippbechhaus@gmail.com_
