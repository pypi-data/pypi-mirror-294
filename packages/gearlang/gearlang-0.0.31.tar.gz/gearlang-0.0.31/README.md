# GearLang

Gear is a logic based compiler for the Gear language.


## Installation

You can install GearLang from pip:
```bash
pip install gearlang
```


## Development

### Building the Rust code
This will compile the Rust code and install it as a python package.

> [!WARNING]
> Make sure to run this into a python virtual environment to avoid conflicts with other packages.

```bash
maturin develop
```


### Production build
```bash
maturin build --release
```




## Troubleshooting

If the CLI is not working, make sure that the Scripts directory of your Python installation is in your PATH. [Here](https://bobbyhadz.com/blog/python-the-script-is-installed-in-which-is-not-on-path) is a guide on how to do it.

---
License - [MIT](./LICENSE)