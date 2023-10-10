#include <iostream>

using namespace std;

int powerOf2(int exponent) {
	int result = 1;
	for (int i = 0; i < exponent; i++) {
		result *= 2;
	}
	return result;
}

template <const int k>
struct Clause {
	int ids[k];
	bool invs[k];
}

template <const int k>
struct Solution {
	bool satisfiable;
	Clause<k> solution;
}

template <int n, int k>
bool solutionExists(Clause<k> clauses[n]) {
	// In conjunctive normal form, the only set of
	// solutions that doesn't work is the set of solutions
	// in which each solution doesn't satisfy at least one
	// of the OR clauses. Thus, there are n "incorrect"
	// solutions and 2^k possible solutions. If the number
	// of incorrect solutions is less than the number of
	// total solutions, then there is AT LEAST one solution
	// which satisfies all of the OR clauses, since that
	// solution is not in the set of incorrect solutions
	// since if n < 2^k then there is at least one solution
	// that DOES add to the 2^k possible solutions and DOES
	// NOT add to the n incorrect solutions, making that
	// solution correct.

	// So, the problem of P vs NP comes down to one
	// exponentiation and a comparison.

	// This algorithm actually works for any number

	// Was this problem supposed to be hard?

	int exponentiation = powerOf2(k);
	return (n < exponentiation);
}

Solution findSolution(Clause<k> clauses[n]) {

}