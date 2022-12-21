import json, os, sys

def list_models():
    return os.listdir('../mlpackages')

def get_vocabs(model_dir):
    file_path = model_dir + '/vocab.json'
    if not os.path.exists(file_path):
        return []
    vocab = json.load(open(file_path, 'r'))
    return vocab

def check_vocab(vocab):
    print('Checking vocab ' + vocab + ' availability...\n')
    has_any = False
    for model in list_models():
        model_dir = '../mlpackages/' + model
        result = get_vocabs(model_dir)
        if vocab in result:
            print('✅ Vocab ' + vocab + ' found in ' + model)
            has_any = True
    if not has_any:
        print('❌ Vocab ' + vocab + ' not found in any model')
    
    print('-----------------------------------------')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python3 check_vocab.py <vocab>')
        sys.exit(1)
    vocab = sys.argv[1]
    check_vocab(vocab)
    check_vocab(vocab + '</w>')
    if ('_' in vocab) or (' ' in vocab):
        check_vocab(vocab.replace('_', '').replace(' ', ''))
        check_vocab(vocab.replace('_', '').replace(' ', '') + '</w>')
