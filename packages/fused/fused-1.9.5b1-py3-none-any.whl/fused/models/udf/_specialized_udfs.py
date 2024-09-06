import warnings
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Literal, Optional, Union, overload

from fused.models.api.job import UdfJobStepConfig
from fused.warnings import FusedUdfWarning

from .base_udf import UdfType
from .udf import GeoPandasUdfV2


class GeoPandasUdfV2Callable(GeoPandasUdfV2):
    type: Literal[UdfType.GEOPANDAS_V2] = UdfType.GEOPANDAS_V2
    """This class is returned from `@fused.udf` and represents
    a UDF that can be instantiated into a job."""

    def to_file(self, where: Union[str, Path, BinaryIO], *, overwrite: bool = False):
        """Write the UDF to disk or the specified file-like object.

        The UDF will be written as a Zip file.

        Args:
            where: A path to a file or a file-like object.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="zip", overwrite=overwrite)

    def to_directory(self, where: Union[str, Path], *, overwrite: bool = False):
        """Write the UDF to disk as a directory (folder).

        Args:
            where: A path to a directory.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="local", overwrite=overwrite)

    def to_gist(self, where: Optional[str] = None, *, overwrite: bool = False):
        """Write the UDF to Github as a Gist.

        Args:
            gist_id: Optionally, a Gist ID to overwrite.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="gist", overwrite=overwrite)

    # This is a subclass of GeoPandasUdfV2 so that the job classes can reference
    # GeoPandasUdfV2 without issues. This class is then installed over the
    # GeoPandasUdfV2 type code so that loaded objects get the __call__ methods.

    # List of data input is passed - run that
    @overload
    def __call__(self, *, arg_list: Iterable[Any], **kwargs) -> UdfJobStepConfig:
        ...

    # Nothing is passed - run the UDF once
    @overload
    def __call__(self, *, arg_list: None = None, **kwargs) -> UdfJobStepConfig:
        ...

    def __call__(
        self, *, arg_list: Optional[Iterable[Any]] = None, **kwargs
    ) -> Union[UdfJobStepConfig,]:
        """Create a job from this UDF.

        Args:
            arg_list: A list of records to pass in to the UDF as input.
        """

        with_params = self.model_copy()
        # TODO: Consider using with_parameters here, and validating that "context" and other reserved parameter names are not being passed.
        new_parameters = {**kwargs}
        if new_parameters:
            with_params.parameters = new_parameters

        if arg_list is not None and not len(arg_list):
            warnings.warn(
                "An empty `arg_list` was passed in, no calls to the UDF will be made.",
                FusedUdfWarning,
            )

        return UdfJobStepConfig(
            udf=with_params,
            input=arg_list,
        )
