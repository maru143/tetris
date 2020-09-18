# Tetris

[![Build Status](https://travis-ci.org/maru143/tetris.svg?branch=master)](https://travis-ci.org/maru143/tetris)
[![codecov](https://codecov.io/gh/maru143/tetris/branch/master/graph/badge.svg)](https://codecov.io/gh/maru143/tetris)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This is a tetris game just for learning Python.

## Running

#### Dependencies

Running this tetris game requires:

- A Python interpreter (version 3.5 or later)

- numpy (version 1.19.2 or later)

- PyQt5



If you have an appropriate Python interpreter, you can install these requirements by running the following at the root directory:

```bash
$ pip install -r requirements.txt 
```



To run tetris, type the following command:

```bash
$ python src/main.py
```



## How to play

You can play using your keyboard:

| key                     | motion     |
| ----------------------- | ---------- |
| →                       | move right |
| ←                       | move left  |
| ↓                       | soft drop  |
| ↑, SPACE                | hard drop  |
| SHIFT                   | hold       |
| z                       | spin left  |
| x                       | spin right |
| p                       | pause      |
| ESC                     | quit game  |



## Functions

This tetris supports the following features:

- [x] Hold
- [x] Next (you can see 5 next minos)
- [x] Bag randomizer
- [ ] Super rotation system
- [ ] T-spin 
- [ ] display scores
- [ ] restart button