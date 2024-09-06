import re
import os
import sys
import argparse

def main(args):
    sbatch_file = args.sbatch_file
    param_file = args.param_file
    max_run_jobs = args.max_run_jobs

    # Check that the sbatch file exists
    if not os.path.exists(sbatch_file):
        print(f"The sbatch file {sbatch_file} does not exist")
        sys.exit(1)

    # Check that the param file exists
    if not os.path.exists(param_file):
        print(f"The param file {param_file} does not exist")
        sys.exit(1)


    all_params = []
    with open(param_file, "r") as f:
        for line in f:
            all_params.append(line.strip())

    # remove any empty lines
    all_params = [x for x in all_params if x]

    with open(sbatch_file, "r") as f:
        sbatch = f.read()

    # Find the number of jobs
    num_jobs = len(all_params)
    if not max_run_jobs:
        max_run_jobs = num_jobs
    else:
        print(f"Max run jobs set to {max_run_jobs}")
        max_run_jobs = min(max_run_jobs, num_jobs)

    # remove the line of the sbatch array option (check for #SBATCH --array=)
    if re.search(r"#SBATCH --array=.*\n", sbatch):
        print("Removing existing #SBATCH --array= line")
        sbatch = re.sub(r"#SBATCH --array=.*\n", "", sbatch)

    # add a new #SBATCH --array= line after the last #SBATCH line
    # find the last #SBATCH line
    last_sbatch_line = sbatch.rfind("#SBATCH")
    # get length of the line
    last_sbatch_line = sbatch.find("\n", last_sbatch_line)
    final_sbatch = sbatch[:last_sbatch_line] + "\n#SBATCH --array=1-" + str(num_jobs)
    if max_run_jobs and max_run_jobs < num_jobs:
        final_sbatch += f"%{max_run_jobs}"
    final_sbatch += "\n" + sbatch[last_sbatch_line:]

    # write the final sbatch file but rename it to add _paramfile to the name. Rename everything before the extension
    sbatch_file_name = os.path.basename(sbatch_file)
    sbatch_file_name_no_ext = os.path.splitext(sbatch_file_name)[0]
    sbatch_file_dir = os.path.dirname(sbatch_file)
    new_sbatch_file = os.path.join(sbatch_file_dir, sbatch_file_name_no_ext + "_paramfile" + os.path.splitext(sbatch_file_name)[1])

    with open(new_sbatch_file, "w") as f:
        f.write(final_sbatch)

    print(f"New sbatch file written to {new_sbatch_file}")
    print(f"Number of jobs: {num_jobs}")
    print(f"Max running jobs: {max_run_jobs}")
    # Print a message to tell the user to run the sbatch file and that they need
    # to add a code that takes the array index and uses it to get the correct
    # parameter from the param file
    print("You will need to add code to your script to read the correct parameter from the param file")
    print("You can use the SLURM_ARRAY_TASK_ID environment variable to get the array index")
    # print a bash example
    print("\nExample bash code that you need to use to get the parameters from the param file:")
    print("-"*100)
    print("args=$(sed -n ${SLURM_ARRAY_TASK_ID}p $1)")
    print("echo \"Running with the following parameters:\"")
    print("echo $args")
    # parse the args into variables
    print("IFS=' ' read -r -a array <<< $args")
    print("var1=${array[0]}")
    print("var2=${array[1]}")
    print("var3=${array[2]}")
    print("-"*100)
    print("You can then run your script with the following command:")
    print(f"sbatch {new_sbatch_file} {param_file}")


def entry_point():
    parser = argparse.ArgumentParser(description="Process sbatch and param files.")
    parser.add_argument("sbatch_file", help="The sbatch file to process")
    parser.add_argument("param_file", help="The parameter file to process")
    parser.add_argument("--max_run_jobs", type=int, default=None, help="The maximum number of jobs to run at once")

    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process sbatch and param files.")
    parser.add_argument("sbatch_file", help="The sbatch file to process")
    parser.add_argument("param_file", help="The parameter file to process")
    parser.add_argument("--max_run_jobs", type=int, default=None, help="The maximum number of jobs to run at once")

    args = parser.parse_args()
    main(args)