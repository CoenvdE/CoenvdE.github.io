---
layout: blog_chapter
title: Python Basics
description: Getting started with Python and basic syntax
date: 2024-05-26
collection: blogs
collection_id: python_tutorial
chapter_number: 1
img: assets/img/11.jpg
importance: 1
category: blog-collection
---

# Python Basics

Welcome to the first chapter of our Python tutorial! In this chapter, we'll cover the basics of Python and get you set up for programming.

## Installing Python

Before we begin, you need to install Python on your computer. You can download the latest version from [python.org](https://python.org).

For Windows users:

1. Download the installer from the official website
2. Run the installer and check "Add Python to PATH"
3. Click "Install Now"

For macOS users:

1. Download the macOS installer from python.org
2. Run the installer package
3. Follow the installation instructions

For Linux users:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Your First Python Program

Let's write the classic "Hello, World!" program:

```python
print("Hello, World!")
```

Save this in a file named `hello.py` and run it:

- On Windows: `python hello.py`
- On macOS/Linux: `python3 hello.py`

## Basic Python Syntax

### Variables and Data Types

```python
# String
name = "John"

# Integer
age = 30

# Float
height = 1.75

# Boolean
is_student = True

# Printing variables
print(name)
print(age)
print(height)
print(is_student)
```

### Basic Operations

```python
# Arithmetic operations
a = 10
b = 5

print(a + b)  # Addition: 15
print(a - b)  # Subtraction: 5
print(a * b)  # Multiplication: 50
print(a / b)  # Division: 2.0
print(a % b)  # Modulus: 0
print(a ** b) # Exponentiation: 100000

# String operations
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)  # John Doe
```

## What's Next?

In the next chapter, we'll learn about control flow in Python, including if statements, loops, and how to make decisions in your code.
