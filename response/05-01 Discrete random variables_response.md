## Discrete Random Variables

### Introduction
- **Instructor**: JinYeong Bak (jy.bak@skku.edu), College of Computing, SKKU
- **Source**: H. Pishro-Nik, "Introduction to probability, statistics, and random processes", Kappa Research LLC, 2014. [Online Resource](https://www.probabilitycourse.com)

### Rationale
- **Purpose**: To analyze random experiments by focusing on their numerical aspects.
- **Examples**: In sports like soccer, interest might lie in the number of goals, shots, corners, fouls, etc.
- **Definition**: A random variable is a real-valued variable determined by an underlying random experiment.

### Random Variables
- **Nature**: Random experiments often yield numerical outputs, such as product lifetimes or gambling winnings.
- **Conversion to Numerical**: Non-numerical events can often be quantified for convenience and analysis.
- **Example**: Tossing a coin five times and observing the number of heads.
- **Formal Definition**: A random variable is a real-valued function on the sample space.
    - **Range**: The set of possible values a random variable can take.
    - **Notation**: Random variables are denoted by capital letters.

### Examples of Random Variables
- **Coin Toss**: Flipping a coin twice and counting the number of heads.
- **Product Lifetime**: Denoted as T, representing the lifetime of a product.

### Countable Sets
- **Finite Set**: A set with a limited number of elements.
- **One-to-One Correspondence with Natural Numbers**: The elements can be listed or matched one-to-one with natural numbers, making it countable.

### Countably Infinite Sets
- **Characteristics**: These sets can be listed but are infinite in size.
- **Countability**: Despite being infinite, these sets are still considered countable.

### Non-Countable Sets
- **Real Numbers**: The set of real numbers is an example of a set that is not countable.

### Discrete Random Variables
- **Definition**: A random variable is discrete if its range is countable.
- **Notation**: The values in the range of a discrete random variable are denoted by lowercase letters.

**End of Lecture**

## Probability Mass Function (PMF)

### Definition
- A **discrete random variable** is a variable that can take on a countable number of distinct values.
- The **Probability Mass Function (PMF)** is a function that gives the probability that a discrete random variable is exactly equal to some value.

### Example 1: Coin Toss
- **Scenario**: Tossing a fair coin twice and counting the number of heads.
- **Range of**: 0, 1, 2 (possible outcomes of heads).
- **PMF**: 
  - P(X=0) = 1/4 (TT)
  - P(X=1) = 1/2 (HT, TH)
  - P(X=2) = 1/4 (HH)

### Example 2: Die Roll
- **Scenario**: Rolling a die until the first 6 appears.
- **Range of**: 1, 2, 3, ... (number of rolls).
- **PMF**: 
  - P(X=k) = (5/6)^(k-1) * (1/6), for k = 1, 2, 3, ...

### Properties of PMF
For a discrete random variable with PMF \(p(x)\) and Range \(R\):
- **a)** \(p(x) \geq 0\) for all \(x\) in \(R\).
- **b)** \(\sum_{x \in R} p(x) = 1\).
- **c)** The probability of any event \(A\) is \(\sum_{x \in A} p(x)\).

### Visualization
- Repeating an experiment and plotting the histogram of outcomes will approximate the PMF.
- **Example 1 Visualization**: Shows probabilities for 0, 1, and 2 heads in a two-coin toss.

## Independent Random Variables

### Definition
- **Two Variables**: Random variables \(X\) and \(Y\) are **independent** if the occurrence of \(X\) does not affect the probability distribution of \(Y\) and vice versa.
- **Formula**: \(P(X \cap Y) = P(X)P(Y)\).
- **Multiple Variables**: \(n\) discrete random variables \(X_1, X_2, ..., X_n\) are **independent** if for any subset of these variables, the joint probability equals the product of their individual probabilities.

## Summary of Random Variables

- **Random Variables**: Can be discrete (countable outcomes) or continuous (uncountable outcomes).
- **Discrete Random Variable**: Takes countable values.
- **PMF**: Describes the probability of each possible value of a discrete random variable.
- **Independent Random Variable**: Two or more variables are independent if the occurrence of one does not affect the probability distribution of the others.

**End of Lecture**