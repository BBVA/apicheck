
from apitest import SharedConfig, String


class ApitestGenerateUnitTestModel(SharedConfig):
    file_path = String()
    output_dir = String()
    
__all__ = ("ApitestGenerateUnitTestModel", )


