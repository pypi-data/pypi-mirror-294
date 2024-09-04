import os
from bbmapy import bbduk, bbmap, reformat, bbmerge

def test_bbduk():
    print("Testing bbduk...")
    bbduk(
        in_file="input.fastq",
        out="output_bbduk.fastq",
        ref="adapters.fa",
        ktrim="r",
        k=23,
        mink=11,
        hdist=1,
        tpe=True,
        tbo=True,
        Xmx="1g"
    )

def test_bbmap():
    print("Testing bbmap...")
    bbmap(
        in_file="input.fastq",
        out="output_bbmap.sam",
        ref="reference.fa",
        Xmx="2g",
        t=4,
        vslow=True
    )

def test_reformat():
    print("Testing reformat...")
    reformat(
        in_file="input.fastq",
        out="output_reformat.fasta",
        fastawrap=80,
        qin=33,
        qout=64
    )

def test_bbmerge():
    print("Testing bbmerge...")
    bbmerge(
        in1="input_1.fastq",
        in2="input_2.fastq",
        out="output_merged.fastq",
        outu1="unmerged_1.fastq",
        outu2="unmerged_2.fastq",
        strict=True,
        k=60,
        extend2=50,
        rem=True,
        Xmx="1g"
    )

def test_capture_output():
    print("Testing output capture...")
    stdout, stderr = bbduk(
        capture_output=True,
        in_file="input.fastq",
        out="output_capture.fastq",
        ref="adapters.fa",
        ktrim="r",
        k=23
    )
    print("Captured stdout:", stdout[:100] + "..." if stdout else "None")
    print("Captured stderr:", stderr[:100] + "..." if stderr else "None")

if __name__ == "__main__":
    try:
        os.mkdir("test")
    except:
        os.chdir("test")
    # Create dummy input files for testing
    with open("input.fastq", "w") as f:
        f.write("@seq1\nACGT\n+\nIIII\n")
    with open("input_1.fastq", "w") as f:
        f.write("@seq1\nACGT\n+\nIIII\n")
    with open("input_2.fastq", "w") as f:
        f.write("@seq1\nTGCA\n+\nIIII\n")
    with open("reference.fa", "w") as f:
        f.write(">ref1\nACGTACGTACGT\n")
    with open("adapters.fa", "w") as f:
        f.write(">adapter1\nACGTACGT\n")

    # Run tests
    test_bbduk()
    test_bbmap()
    # test_reformat()
    test_bbmerge()
    test_capture_output()

    stdout, stderr = bbduk(
            capture_output=True,
            in_file="phiX174.fasta",
            out="output_capture.fastq",
            ref="phix",
            ktrim="r",
            k=23
        )
    # Clean up dummy files
    for file in ["input.fastq", "input_1.fastq", "input_2.fastq", "reference.fa", "adapters.fa",
                 "output_bbduk.fastq", "output_bbmap.sam", "output_reformat.fasta", 
                 "output_merged.fastq", "unmerged_1.fastq", "unmerged_2.fastq", "output_capture.fastq"]:
        if os.path.exists(file):
            os.remove(file)

    print("All tests completed.")
