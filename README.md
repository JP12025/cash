# Cash

![some coins](https://4.bp.blogspot.com/-H754wB9V3kA/UnAmo0rfwUI/AAAAAAAACbI/TWQineE6nvw/s400/eurocoins.png)

# What to Do

Suppose you work in a shop and a child buys a candy for 0.36€.
He gives you a `1€` coin, so you have to give him `64` cents back. 
Knowing that you have coins of `50`, `20`, `10`, `5`, `2` and `1` cents, you have several ways of giving change.
For instance, `2x20 + 2x10 + 1x2 + 2x1` which uses 7 coins or `3x20 + 1x2 + 2x1` which uses 6 coins or `3x20 + 2x2` which uses 5 coins or `1x50 + 1x10 + 2x2` which uses 4 coins.

In a file called `cash.py`, implement a program that prints the minimum coins needed to make the given amount of change, in cents, as in the below:

```bash
$ python cash.py
Amount: 64
4
```

> [!TIP]
> To transform `str` into `int`, simply use `int()`.

Re-prompt the user, again and again as needed, if their input is not between 1 and 99 included (or if their input isn’t an int at all!).

```bash
$ python cash.py
Amount: 103
Amount: -2
Amount: 26
3
```

> [!TIP]
> How many times `25` appears in `64`? Well as simple as `64 // 25` (and you're left with `64 % 25`)

# When to Do it

By Sunday, january 12, 2025 at 11:59 PM

# How to Test

- Test your script with command `./check [-v] cash.py`
- `-v` option gives the difference between what is expected and what your script prints

What happens if the user input is :
* `-1` ?
* `0` ?
* `1` ?
* `4` ?
* `5` ?
* `24` ?
* `99` ?
* `127` ?

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle
