import sys, getopt, subprocess, json, os, hashlib

def get_args(argv):
    args_dir = ''
    prompt = ''
    negative_prompt = ''
    step = '30'
    opts, args = getopt.getopt(argv, "", ["args-dir=", "prompt=", "negative-prompt=", "seed=", "step="])
    for opt, arg in opts:
        if opt in ("--args-dir"):
            args_dir = arg
        elif opt in ("--prompt"):
            prompt = arg
        elif opt in ("--negative-prompt"):
            negative_prompt = arg
        elif opt in ("--seed"):
            seed = arg
        elif opt in ("--step"):
            step = arg

    if args_dir == '':
        print('No args dir given')
        sys.exit(1)
    elif seed == '':
        print('No seed given')
        sys.exit(1)

    output_dir = '../output/'
    dir = output_dir + '/' + args_dir
    orig_prompt, orig_negative_prompt, model, scheduler = load_args(dir)

    if prompt == '':
        prompt = orig_prompt
    if negative_prompt == '':
        negative_prompt = orig_negative_prompt

    hash = hashlib.md5((prompt + negative_prompt).encode('utf-8')).hexdigest()[:8]
    new_dir = makedir(dir, hash)

    record_args(new_dir, prompt, negative_prompt, model, step, scheduler)
    run_pipeline(new_dir, prompt, negative_prompt, model, seed, step, scheduler)

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

def makedir(dir_name, hash):
    dir = dir_name + '/seed_editing_' + hash
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def record_args(save_dir, prompt, negative_prompt, model, step, scheduler):
    data = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "model": model,
        "step": step,
        "scheduler": scheduler
    }
    f = open(save_dir + "/args.json", "w")
    f.write(json.dumps(data, sort_keys=True, indent=4))

def run_pipeline(save_dir, prompt, negative_prompt, model, seed, step, scheduler):
    result = subprocess.run([
    "swift", "run", "StableDiffusionSample", 
    prompt, 
    negative_prompt, 
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
