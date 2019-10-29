# graphvisualizer

## Dependencies

```.
pip install networkx
pip install matplotlib
```

## Usage

```.
cd src
# create examles
python example_nets.py -n 5
# run visualizer
python vis_static.py
# open ./nets
```

```.
% python vis_static.py -h
usage: vis_static.py [-h] [-s S] [-f F] [-t T] [-g {circ,fruc,rand}] [-v V]
Visualizes networks static.

optional arguments:
  -h, --help  show this help message and exit
  -s S        figure size (default=5)
  -f F        file
  -t T        out file type (default="pdf")
  -v V        create images (default="true")
  -g G        choose only one graph type ({circ,fruc,rand})

```

### Contributions are welcome.
