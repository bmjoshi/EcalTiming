
# Check input files
files = os.popen('dasgoclient --query=\'file dataset='+args.inputDataset+'\'').readlines()

runs = []
for file_ in files:
    print("Querying runs for file {}".format(file_))
    file_ = file_.strip('\r\n')
    run_ = os.popen('dasgoclient --query=\'run file='+file_+'\'').readlines()
    if run_ not in runs: runs.append(run_)

