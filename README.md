# Convert3D Nipype Interface
### Contents
Nipype interfaces for c3d and c3d_affine_tool

### Why?
If you use ANTs for registration and then transform the resulting warp fields to FSL format for ICA-AROMA, the Nipype interfaces for Convert3D do not have all the functionalities needed to be able to use them as a node in a workflow for this specific purpose. Therefore, I made some very minimalistic wrappers for c3d and c3d_affine_tool. They are meant for this one specific thing only but maybe it saves someone else some time :)

### Example
    >>> myc3 = MyC3d()
    >>> myc3.inputs.in_file = output1Warp
    >>> myc3.inputs.out_files = ("ants_str2Template_wx.nii.gz", "ants_str2Template_wy.nii.gz", "ants_str2Template_wz.nii.gz")
    >>> myc3.cmdline
    'c3d -mcs transform1Warp.nii.gz -oo ants_str2Template_wx.nii.gz ants_str2Template_wy.nii.gz ants_str2Template_wz.nii.gz'
    
    >>> myc3tool = MyC3dAffineTool()
    >>> myc3tool.inputs.reference_file = 'standard.nii.gz'
    >>> myc3tool.inputs.source_file = 'highres.nii.gz'
    >>> myc3tool.inputs.itk_transform = "transform0GenericAffine.mat"
    >>> myc3tool.inputs.out_file = 'ants_str2Template_affine_flirt.mat'
    >>> myc3tool.inputs.ras2fsl = True
    >>> myc3tool.cmdline
    'c3d_affine_tool -ref standard.nii.gz -src highres.nii.gz -itk transform0GenericAffine.mat -ras2fsl -o ants_str2Template_affine_flirt.mat'
    
