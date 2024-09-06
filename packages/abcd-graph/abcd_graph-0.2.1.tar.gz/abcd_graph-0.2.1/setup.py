# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abcd_graph',
 'abcd_graph.api',
 'abcd_graph.callbacks',
 'abcd_graph.core',
 'abcd_graph.core.abcd_objects']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.4,<2.0.0',
 'pydantic>=2.6.4,<3.0.0',
 'typing-extensions>=4.10.0,<5.0.0']

extras_require = \
{'all': ['pre-commit>=3.7.0,<4.0.0',
         'pytest>=8.1.1,<9.0.0',
         'pytest-cov>=5.0.0,<6.0.0',
         'networkx>=3.3,<4.0',
         'igraph',
         'matplotlib>=3.9.0,<4.0.0',
         'scipy>=1.0.0,<2.0.0'],
 'dev': ['pre-commit>=3.7.0,<4.0.0',
         'pytest>=8.1.1,<9.0.0',
         'pytest-cov>=5.0.0,<6.0.0'],
 'igraph': ['igraph'],
 'matplotlib': ['matplotlib>=3.9.0,<4.0.0'],
 'networkx': ['networkx>=3.3,<4.0'],
 'scipy': ['scipy>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'abcd-graph',
    'version': '0.2.1',
    'description': 'A python library for generating ABCD graphs.',
    'long_description': '# abcd-graph\nA python library for generating ABCD graphs.\n\n## Installation\n```bash\npip install abcd-graph\n```\n\n## Usage\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params, n=1000, logger=True).build()\n```\n\n### Parameters\n\n- `params`: An instance of `ABCDParams` class.\n- `n`: Number of nodes in the graph.\n- `logger` A boolean to enable or disable logging to the console. Default is `False` - no logs are shown.\n- `callbacks`: A list of instances of `Callback` class. Default is an empty list.\n\n### Returns\n\nThe `Graph` object with the generated graph.\n\n### Graph generation parameters - `ABCDParams`\n\nThe `ABCDParams` class is used to set the parameters for the graph generation.\n\nArguments:\n\n| Name    | Type    | Description                                              | Default |\n|---------|---------|----------------------------------------------------------|---------|\n| `gamma` | `float` | Power-law parameter for degrees, between 2 and 3         | 2.5     |\n| `delta` | `int`   | Min degree                                               | 5       |\n| `zeta`  | `float` | Parameter for max degree, between 0 and 1                | 0.5     |\n| `beta`  | `float` | Power-law parameter for community sizes, between 1 and 2 | 1.5     |\n| `s`     | `int`   | Min community size                                       | 20      |\n| `tau`   | `float` | Parameter for max community size, between zeta and 1     | 0.8     |\n| `xi`    | `float` | Noise parameter, between 0 and 1                         | 0.25    |\n\nParameters are validated when the object is created. If any of the parameters are invalid, a `ValueError` will be raised.\n\n### Exporting\n\nExporting the graph to different formats is done via the `exporter` property of the `Graph` object.\n\nPossible formats are:\n\n| Method                         | Description                                                                               | Required packages | Installation command         |\n|--------------------------------|-------------------------------------------------------------------------------------------|-------------------|------------------------------|\n| `to_networkx()`                | Export the graph to a `networkx.Graph` object.                                            | `networkx`        | `pip install abcd[networkx]` |\n| `to_igraph()`                  | Export the graph to an `igraph.Graph` object.                                             | `igraph`          | `pip install abcd[igraph]`   |\n| `adj_matrix`                   | Export the graph to a `numpy.ndarray` object representing the adjacency matrix.           |                   |                              |\n| `to_sparse_adjacency_matrix()` | Export the graph to a `scipy.sparse.csr_matrix` object representing the adjacency matrix. | `scipy`           | `pip install abcd[scipy]`    |\n| `to_edge_list()`               | Export the graph to a list of tuples representing the edges.                              |                   |                              |\n\n\nExample:\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params, n=1000, logger=True).build()\ngraph_networkx = graph.exporter.to_networkx()\n```\n\n\n### Callbacks\n\nCallbacks are used to handle diagnostics and visualization of the graph generation process. They are instances of the `ABCDCallback` class.\n\nOut of the box, the library provides three callbacks:\n- `StatsCollector` - Collects statistics about the graph generation process.\n- `PropertyCollector` - Collects properties of the graph.\n- `Visualizer` - Visualizes the graph generation process.\n\nExample:\n```python\n\nfrom abcd_graph import Graph, ABCDParams\n\nfrom abcd_graph.callbacks import StatsCollector, Visualizer, PropertyCollector\n\n\nstats = StatsCollector()\nvis = Visualizer()\nprops = PropertyCollector()\nparams = ABCDParams()\ng = Graph(params, n=1000, logger=True, callbacks=[stats, vis, props]).build()\n\nprint(stats.statistics)\n\nprint(props.xi_matrix)\n\nvis.draw_community_cdf()\n```\n',
    'author': 'Aleksander Wojnarowicz',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AleksanderWWW/abcd-graph',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
