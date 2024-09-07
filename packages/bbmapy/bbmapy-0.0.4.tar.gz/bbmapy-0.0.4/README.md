# bbmapy

A Python wrapper for BBTools.

## Installation
1. Lazy way - Clone this repository, download bbmap, and install the package:
   ```
   git clone https://github.com/urineri/bbmapy.git
   cd bbmapy
   cd vendor
   rm bb* -rf
   wget https://sourceforge.net/projects/bbmap/files/latest/download -O bbtools.tar.gz
   tar -xf bbtools.tar.gz
   cd ..
   pip install -e .
   generate-bbmapy-commands
   ```
   The above should be automatically done if you are installing from pip (pypi)
   
2. Unlazy way - is commented out below this line, that's how much it isn't suggested.
<!-- Add the BBTools submodule:
   ```
   git submodule add https://bitbucket.org/berkeleylab/jgi-bbtools.git vendor/bbtools
   ```

3. Initialize and update the submodule:
   ```
   git submodule init
   git submodule update
   ```

4. Install the package:
   ```
   pip install .
   ```

5. Generate the commands:
   ```
   generate-ppby-commands
   ```
6. Now actually delete the git submodule in vendor and replace it with the sourceforge version (i.e. the lazy way):
```
cd vendor/
rm bb* -rf
wget https://sourceforge.net/projects/bbmap/files/latest/download -O bbtools.tar.gz
tar -xf bbtools.tar.gz

``` -->
<!-- 
Note: Steps 2 and 3 are only necessary if you're setting up the project for the first time or if the submodule hasn't been added yet. If you're cloning the repository and the submodule has already been added, you can use: -->
<!-- 
```
git clone --recurse-submodules https://github.com/yourusername/ppby.git
```

This will clone the repository and initialize the submodule in one step... I think? -->



## Dependencies
- Java  
- BBmap  (the above steps should download it to the vendor subdirectory...).  
If you rather this to use your own bbmap etc, go to the base.py script and comment out line 51, then uncomment line 52.
- rich (for pretty printing)

## Usage

After installation, you can use ppby in your Python scripts like this:

```python
from ppby import bbduk

# Basic usage
bbduk(
    in_file="input.fastq",
    out="output.fastq",
    ktrim="r",
    k="23",
    mink="11",
    hdist="1",
    tbo=True,
    tpe=True,
    minlen="45",
    ref="adapters",
    ftm="5",
    maq="6",
    maxns="1",
    ordered=True,
    threads="4",
    overwrite="t",
    stats="stats.txt"
)

# Using Java flags alongside other arguments
bbduk(
    Xmx="2g",  # Set maximum heap size
    da=True,   # Enable assertions
    eoom=True, # Enable out-of-memory termination
    in_file="input.fastq",
    out="output.fastq",
    ktrim="r",
    k="23"
)

# To capture output
stdout, stderr = bbduk(
    capture_output=True,
    Xmx="2g",
    in_file="input.fastq",
    out="stdout.fastq",
    # ... other parameters ...
)
```

#### Notes:
 * `in` can be a protected word in python and other code, it is replaced by `in_file` in function calls. `in1`, `in2` are still valid.
 * Java flags (such as `Xmx`, `Xms`, `da`, `ea`, `eoom`) are automatically recognized and handled appropriately. Include them in your function calls just like any other argument.
 * the `capture_output` argument might be switched (stderr --> out and vice verse). 
 
### Citation
BBMerge manuscript: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0185056
Please cite this paper if you use bbmap in your work.



## License

This project is only a wrapper, please see the actual bbtools repository for (license)[https://bitbucket.org/berkeleylab/jgi-bbtools/src/master/license.txt] etc.  
Neither the developers of bbtools nor of ppby take any responsibility for how you use this code. All accountability is on you.

## Acknowledgments

This project only (crudely) wraps BBTools (a.k.a bbmap), which is developed by Brian Bushnell.  
If you use ppby and things don't quite work like you'd like, don't expect the developer of bbmap to help you with this whacky python wrapper.  
If 
Please see the [BBTools website](https://jgi.doe.gov/data-and-tools/bbtools/) for more information about the underlying tools.  
