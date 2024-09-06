# Create sbatch Array Job with the same size as a parameter file

This script creates a sbatch array job with the same size as a parameter file. The parameter file is a text file with one line per job. The script reads the parameter file and creates a sbatch array job with the same number of jobs as lines in the parameter file, with the option to specify the maximum number of jobs to run concurrently.

This is similar to `oarsub --array-param-file <file>` in OAR. But it won't launch the jobs automatically, you need to submit the job array manually.

## Usage

First make sure that your script has a logic that takes in the job index from slurm and reads the corresponding line from the parameter file. For example add this to your script:

```bash
args=$(sed -n ${SLURM_ARRAY_TASK_ID}p $1)
echo "Running with the following parameters:"
echo $args
IFS=' ' read -r -a array <<< $args
var1=${array[0]}
var2=${array[1]}
var3=${array[2]}

echo "var1: $var1"
echo "var2: $var2"
echo "var3: $var3"
```

Then run the tool to create the sbatch script from an existing sbatch file and a parameter file:

```bash
sbatch_paramfile <sbatch_file> <param_file> --max_run_jobs <max_run_jobs>
```

This will create a new sbatch file with the same name as the original sbatch file, but with `_paramfile` appended to the name. This new sbatch file will have the same number of jobs as lines in the parameter file, and it will add the `#SBATCH --array=1-<number_of_jobs>%<max_run_jobs>` line to the sbatch file.

Then submit the job array:

```bash
sbatch <output_sbatch_file> <param_file>
```

# Contact
- [Wissam Antoun](https://github.com/WissamAntoun/)