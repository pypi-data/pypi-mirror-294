import shutil
import subprocess as sp
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
import os
from tests import common

def test_phyfum_tree_mode():
    tmpdir = "/tmp/"
    workdir = Path(tmpdir) / "phyfum_test"
    #expected_path = PurePosixPath("tests/expected")
    result_path = PurePosixPath(f"{workdir}/test_run")
    inp = Path("tests/data/exampleBeta.csv").absolute()
    patientinfo = Path("tests/data/metadata.csv").absolute()
    
    # Copy data to the temporary workdir.
    expected_workdir = workdir 
    #shutil.copytree(expected_path, expected_workdir)
    
    # Run the test job.
    rr = sp.run([
        "phyfum", 
        "run", 
        "--input", inp, 
        "--patientinfo", patientinfo, 
        "--output", "na", 
        "--iterations", "400", 
        "--workdir", result_path, 
        "--stemcells", "2-4-1", 
        "--nchains", "1", 
        "--sampling", "1", 
        "--notemp"
        ],
        stdout=sp.DEVNULL, stderr=sp.DEVNULL
    )
    assert rr.returncode == 0

    # Compare the result with the expected output 
    #common.OutputChecker(result_path, expected_path, workdir).check() # TODO: some files have times and dates, invalidating the results... 