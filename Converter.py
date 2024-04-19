import sys
from nfstream import NFStreamer


path = sys.argv[1]
new_path = path.split("/")[-1].split(".")
new_path[-1] = "csv"
new_path = ".".join(new_path)

print("File", path, "converted into flow file", new_path)

offline_streamer = NFStreamer(source=path, statistical_analysis=True)
n_flows = offline_streamer.to_csv(path=new_path)
