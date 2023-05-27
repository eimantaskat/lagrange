
## How to use it?
To enter the python console:
```console
> cd <root of the project>
> python3
```

When entered the python3 console:
```console
>>> from lagrange import optimize
>>> result = optimize('-xyz', ['2xy + 2xz + 2yz - 1'], ['-x', '-y', '-z'], [0, 0, 0])  # Should return the xyz for best value.
>>> [0.4082058 0.40828511 0.408254 ]
```
