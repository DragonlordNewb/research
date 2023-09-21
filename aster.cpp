#include <iostream>
#include <cmath>

using namespace std;

// UTILITIES 

class Vector {
	private:
		long double x;
		long double y;
		long double z;
	public:
		Vector(long double _x, long double _y, long double _z) {
			x = _x;
			y = _y;
			z = _z;
		}

		Vector operator+(Vector const& obj) {
			long double xn = x + obj.x;
			long double yn = y + obj.y;
			long double zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator-(Vector const& obj) {
			long double xn = x + obj.x;
			long double yn = y + obj.y;
			long double zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator*(long double f) {
			long double xn = x * f;
			long double yn = y * f;
			long double zn = z * f;
			return Vector(xn, yn, zn);
		}

		long double magnitude() {
			return sqrt(powf(x, 2) + powf(y, 2) + powf(z, 2));
		}
};

int main(int argc, char* argv[]) {
	cout << "Advanced SpaceTime Simulation Software starting up ...\n";

	Vector v1 = Vector(0, 1, 0);
	Vector v2 = Vector(1, 0, 0);
	Vector v3 = v1 + v2;
	cout << v3.magnitude();
}