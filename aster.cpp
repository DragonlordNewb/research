#include <iostream>
#include <cmath>

using namespace std;

// UTILITIES 

class Vector {
	private:
		double x;
		double y;
		double z;
	public:

		Vector() : x(0.0), y(0.0), z(0.0) {}
		
		Vector(double _x, double _y, double _z) {
			x = _x;
			y = _y;
			z = _z;
		}

		Vector operator+(Vector const& obj) {
			double xn = x + obj.x;
			double yn = y + obj.y;
			double zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator-(Vector const& obj) {
			double xn = x - obj.x;
			double yn = y - obj.y;
			double zn = z - obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator*(double f) {
			double xn = x * f;
			double yn = y * f;
			double zn = z * f;
			return Vector(xn, yn, zn);
		}

		double magnitude() {
			return sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
		}
};

class Atom {
	public:
		double energy;
		double charge;
		Vector location;

		Atom(double _energy, double _charge, Vector _location) {
			energy = _energy;
			charge = _charge;
			location = _location;
		}
};

class Body {
	protected:
		double energy;
		double charge;
		Vector location;
		Vector velocity;

	public:
		Body(double _energy, double _charge, Vector _location, Vector _velocity) {
			energy = _energy;
			charge = _charge;
			location = _location;
			velocity = _velocity;
		}

		Atom points() {
			throw invalid_argument("Can\'t use a base Body class for this.");
		}
};

int main(int argc, char* argv[]) {
	cout << "Advanced SpaceTime Simulation Software starting up ...\n";

	Vector v1 = Vector(0, 1, 0);
	Vector v2 = Vector(1, 0, 0);
	Vector v3 = v1 + v2;
	cout << v3.magnitude();
}