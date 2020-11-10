import csrgraph as cg
import nodevectors
import argparse

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

def main(args):
    g = cg.read_edgelist(args.input, sep='\t')
    mdl = nodevectors.Node2Vec(n_components=args.dimensions, walklen=args.walk_length, 
                               epochs=args.num_walks, threads=args.workers, 
                               return_weight=args.p, neighbor_weight=args.q, 
                               w2vparams={'iter': args.iter})
    mdl.fit(g)
    mdl.model.wv.save_word2vec_format(args.output)

if __name__ == "__main__":
    main(parse_args())
