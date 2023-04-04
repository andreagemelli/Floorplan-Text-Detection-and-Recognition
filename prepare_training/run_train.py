import sys
#sys.path.insert(0, '/home/gemelli/dmp')
from txt_det.ctpn.train_net import train_network

if __name__ == "__main__":
    # train_path=sys.argv[1]
    # name of the output path of results
    train_path='first_train'
    train_network(train_path)

