"""Convert3D is a command-line tool for converting 3D images between common file formats."""

from nipype.interfaces.base import (
    TraitedSpec,
    CommandLineInputSpec,
    SEMLikeCommandLine,
    File,
    InputMultiPath,
    OutputMultiPath,
    CommandLine,
    isdefined
)
import traits.api as traits
import os

    
class CustomC3dAffineToolInputSpec(CommandLineInputSpec):
    reference_file = File(exists=True, argstr="-ref %s", position=1)
    source_file = File(exists=True, argstr="-src %s", position=2)
    transform_file = File(exists=True, argstr="%s", position=3)
    itk_transform = traits.Either(
        traits.Bool,
        File(),
        hash_files=False,
        desc="Export ITK transform.",
        argstr="-itk %s",
        position=4,
    )
    ras2fsl = traits.Bool(argstr="-ras2fsl", position=5)
    out_file = File(
        exists=False,
        argstr="-o %s",
        position=-1,
        desc="Output file",
    )
  
    
class CustomC3dAffineToolOutputSpec(TraitedSpec):
    out_file = File(exists=True)


class CustomC3dAffineTool(SEMLikeCommandLine):
    """Converts ANTS-style itk matrix into fsl/ICA-Aroma compatible format

    Example
    =======
    >>> myc3tool = MyC3dAffineTool()
    >>> myc3tool.inputs.reference_file = 'standard.nii.gz'
    >>> myc3tool.inputs.source_file = 'highres.nii.gz'
    >>> myc3tool.inputs.itk_transform = "transform0GenericAffine.mat"
    >>> myc3tool.inputs.out_file = 'ants_str2Template_affine_flirt.mat'
    >>> myc3tool.inputs.ras2fsl = True
    >>> myc3tool.cmdline
    'c3d_affine_tool -ref standard.nii.gz -src highres.nii.gz -itk transform0GenericAffine.mat -ras2fsl -o ants_str2Template_affine_flirt.mat'
    
    """
    input_spec = MyC3dAffineToolInputSpec
    output_spec = MyC3dAffineToolOutputSpec

    _cmd = 'c3d_affine_tool'
    _outputs_filenames = {'out_file': 'affine.mat'}
    
  

class CustomC3dInputSpec(CommandLineInputSpec):
    in_file = File(
        position=1,
        argstr="-mcs %s",
        mandatory=True,
        desc="Input file (wildcard and multiple are supported).",
    )
    out_files = InputMultiPath(
        File(),
        exists=False,
        argstr="-oo %s",
        position=-1,
        desc=(
            "Write all images on the convert3d stack as multiple files."
            " Supports both list of output files or a pattern for the output"
            " filenames (using %d substitution)."
        ),
    )



class CustomC3dOutputSpec(TraitedSpec):
    out_files = OutputMultiPath(File())


class Custom3d(CommandLine):
    """
    Convert3d is a command-line tool for converting 3D (or 4D) images between
    common file formats. The tool also includes a growing list of commands for
    image manipulation, such as thresholding and resampling. The tool can also
    be used to obtain information about image files. More information on
    Convert3d can be found at:
    https://sourceforge.net/p/c3d/git/ci/master/tree/doc/c3d.md
    
    This specific wrapper only allows for the -mcs setting, splitting of multi-component images.

    Example
    =======

    >>> myc3 = MyC3d()
    >>> myc3.inputs.in_file = output1Warp
    >>> myc3.inputs.out_files = ("ants_str2Template_wx.nii.gz", "ants_str2Template_wy.nii.gz", "ants_str2Template_wz.nii.gz")
    >>> myc3.cmdline
    'c3d -mcs transform1Warp.nii.gz -oo ants_str2Template_wx.nii.gz ants_str2Template_wy.nii.gz ants_str2Template_wz.nii.gz'
    """

    input_spec = MyC3dInputSpec
    output_spec = MyC3dOutputSpec

    _cmd = "c3d"

    def _list_outputs(self):
        outputs = self.output_spec().get()
        if isdefined(self.inputs.out_files):
            _out_files = [
                os.path.abspath(f)
                for f in self.inputs.out_files
                if os.path.exists(os.path.abspath(f))
            ]
        outputs["out_files"] = _out_files

        return outputs

