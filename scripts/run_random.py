import sys, getopt, subprocess, random, hashlib, os, json

def get_args(argv):
    negative_prompt = ''
    image_count = '1'
    step = '30'
    scheduler = 'pndm'
    opts, args = getopt.getopt(argv, "", ["prompt=", "negative-prompt=", "model=", "image-count=", "step=", "scheduler="])
    for opt, arg in opts:
        if opt in ("--prompt"):
            prompt = arg
        elif opt in ("--negative-prompt"):
            negative_prompt = arg
        elif opt in ("--model"):
            model = arg
        elif opt in ("--image-count"):
            image_count = arg
        elif opt in ("--step"):
            step = arg
        elif opt in ("--scheduler"):
            scheduler = arg

    if prompt == '':
        print('No prompt given')
        sys.exit(1)
    elif model == '':
        print('No model given')
        sys.exit(1)

    hash = hashlib.md5((prompt + negative_prompt).encode('utf-8')).hexdigest()[:8]
    dir_name = (hash + '_' + prompt)[:128] + '_' + model
    new_dir = makedir(dir_name)
    record_args(new_dir, prompt, negative_prompt, model, step, scheduler)
    run_pipeline(new_dir, prompt, negative_prompt, model, image_count, step, scheduler)

def makedir(dir_name):
    output_dir = '../output/'
    dir = output_dir + '/' + dir_name
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
    

def run_pipeline(save_dir, prompt, negative_prompt, model, image_count, step, scheduler):
    result = subprocess.run([
    "swift", "run", "StableDiffusionSample", 
    prompt, 
    "--negative-prompt", negative_prompt,
    "--output-path", save_dir, 
    "--compute-units", "cpuAndGPU",
    "--disable-safety",
    "--image-count", image_count,
    "--seed", str(random.randint(0, 2147483647)),
    "--resource-path", "../mlpackages/" + model,
    "--step-count", step,
    "--scheduler", scheduler,
    "--increment-seed"
    ], stderr=subprocess.PIPE, text=True)
    print(result.stderr)


if __name__ == "__main__":
   get_args(sys.argv[1:])
