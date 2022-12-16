import sys, getopt, subprocess, json, os

def get_args(argv):
    args_dir = ''
    step_low = str(30)
    step_high = str(50)
    interval = str(5)
    scheduler = 'pndm'
    opts, args = getopt.getopt(argv, "", ["args-dir=", "seed=", "step-low=", "step-high=", "interval="])
    for opt, arg in opts:
        if opt in ("--args-dir"):
            args_dir = arg
        elif opt in ("--seed"):
            seed = arg
        elif opt in ("--step-low"):
            step_low = arg
        elif opt in ("--step-high"):
            step_high = arg
        elif opt in ("--interval"):
            interval = arg

    if args_dir == '':
        print('No args dir given')
        sys.exit(1)
    elif seed == '':
        print('No seed given')
        sys.exit(1)
    elif int(step_low) > int(step_high):
        print('Step low is higher than step high')
        sys.exit(1)

    output_dir = '../output/'
    dir = output_dir + '/' + args_dir
    prompt, negative_prompt, model, scheduler = load_args(dir)
    step_dir = makedir(dir, seed)

    for step in range(int(step_low), int(step_high), int(interval)):
        print('Running image with step ' + str(step) + ' of ' + step_high)
        run_pipeline(step_dir, prompt, negative_prompt, model, seed, step, scheduler)

def load_args(dir_name):
    if not os.path.exists(dir_name + '/args.json'):
        print('No args.json found')
        sys.exit(1)
    
    with open(dir_name + '/args.json') as f:
        data = json.load(f)
        prompt = data['prompt']
        negative_prompt = data['negative_prompt']
        model = data['model']
        scheduler = data['scheduler']
        return prompt, negative_prompt, model, scheduler

def makedir(dir_name, seed):
    dir = dir_name + '/seed_' + seed + '_steps'
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def run_pipeline(save_dir, prompt, negative_prompt, model, seed, step, scheduler):
    result = subprocess.run(["time", "swift", "run", "StableDiffusionSample", prompt, negative_prompt, 
    "--output-path", save_dir, 
    "--compute-units", "cpuAndGPU",
    "--disable-safety",
    "--image-count", "1",
    "--seed", seed,
    "--resource-path", "../mlpackages/" + model,
    "--step-count", str(step),
    "--scheduler", scheduler,
    ], stderr=subprocess.PIPE, text=True)
    print(result.stderr)


if __name__ == "__main__":
   get_args(sys.argv[1:])
