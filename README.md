# Convert3D Nipype Interface
### Contents
Nipype interfaces for c3d and c3d_affine_tool

### Why?
If you use ANTs for registration and then transform the resulting warp fields to FSL format for ICA-AROMA, the Nipype interfaces for Convert3D do not have all the functionalities needed to be able to use them as a node in a workflow for this specific purpose. Therefore, I made some very minimalistic wrappers for c3d and c3d_affine_tool. They are meant for this one specific thing only but maybe it saves someone else some time :)

### Example
