import csrgraph as cg
import nodevectors
import argparse
import io
from time import time
from contextlib import redirect_stdout

def parse_args():
    parser = argparse.ArgumentParser(description="Run node2vec using nodevectors.")
    parser.add_argument('--input', nargs='?', help='Input graph path')
    parser.add_argument('--output', nargs='?', help='Output path')
    parser.add_argument('--dimensions', type=int, default=128, help="Embedding dimension")
    parser.add_argument('--walk-length', type=int, default=80, help="Length of walk")
    parser.add_argument('--num-walks', type=int, default=10, help="Number of walks")
    parser.add_argument('--iter', type=int, default=1, help="Epochs in SGD")
    parser.add_argument('--workers', type=int, default=0, help="Number of workers, 0 is full")
    parser.add_argument('--p', type=float, default=1, help="Return parameter")
    parser.add_argument('--q', type=float, default=1, help="Inout parameter")
    return parser.parse_args()

def convert_outstr(outstr):
    walk_time = 0
    train_time = 0

    walk_done = False
    train_done = False

    outstr_lines = outstr.split('\n')
    for line in outstr_lines:
        if ('Making walks' in line) | ('Mapping Walk Names' in line): 
            walk_time += float(line.split('=')[-1])
            walk_done = True
        if 'Training W2V' in line:
            train_time += float(line.split('=')[-1])
            train_done = True

    if walk_done:
        print("Took 00:00:00.00 to pre-compute transition probabilities")
        print("Took %02d:%02d:%05.2f to generate walks"%(walk_time//3600, walk_time%3600//60, walk_time%60))
    if train_done:
        print("Took %02d:%02d:%05.2f to train embeddings"%(train_time//3600, train_time%3600//60, train_time%60))


def main(args):
    t = time()
    g = cg.read_edgelist(args.input, sep='\t')
    load_time = time() - t
    print("Took %02d:%02d:%05.2f to load graph"%(load_time//3600, load_time%3600//60, load_time%60))

    f = io.StringIO()
    mdl = nodevectors.Node2Vec(n_components=args.dimensions, walklen=args.walk_length, 
                               epochs=args.num_walks, threads=args.workers, 
                               return_weight=args.p, neighbor_weight=args.q, 
                               w2vparams={'iter': args.iter})
    with redirect_stdout(f):
        mdl.fit(g)
    convert_outstr(f.getvalue())
    mdl.model.wv.save_word2vec_format(args.output)

if __name__ == "__main__":
    main(parse_args())
