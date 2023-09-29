#include <iostream>

struct LuxSATClause {

	bool x; // false <=> x is negated
	bool y; // false <=> y is negated
	bool z; // false <=> z is negated

	char asNumber() {
		char r = 0;
		if (x) {
			r += 4;
		}
		if (y) {
			r += 2;
		}
		if (z) {
			r += 1;
		}
		return (r);
	}
};

template <int n>
class LuxSAT {

	public:

		LuxSATClause clauses[n];

		LuxSAT(LuxSATClause _clauses[n]) {
			for (int i = 0; i < n; i++) {
				clauses[i] = _clauses[i];
			}
		}

		bool satisfiable() {
			char exclusions = 0;

			for (int i; i < n; i++) {
				exclusions |= clauses[i].asNumber();

				if (exclusions == 255) {
					return false;
				}
			}

			return true;
		}
};

int main() {}
