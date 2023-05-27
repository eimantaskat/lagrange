
# Lagrange

This project is an example repository for lagrange optimization solution.

## Built with
This project was built with Python in VSCode environment. It uses a few non standard libraries such as numpy and sympy.


## How to use it?
To enter the python console:
```console
> cd <root of the project>
> python3
```

When entered the python3 console:
```console
>>> from lagrange import optimize
>>> result = optimize('-x*y*z', ['2*x*y + 2*x*z + 2*y*z - 1'], ['-x', '-y', '-z'], [0, 0, 0])  # Should return the xyz for best value.
>>> [0.4082058 0.40828511 0.408254 ]
```

## Report
*The report of the project can be found as a [pdf in the root of the project repository](./report.pdf) or [here](https://vult-my.sharepoint.com/:w:/g/personal/hubertas_klangauskas_mif_stud_vu_lt/EVfN6D5fSFVCknpfbOsEdlIB5GgwjjL8o5_DSzVA8iVsbQ?e=9IM0uO)*

## Built for
VU Optimization methods group task
