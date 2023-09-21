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

// BASE CLASSES

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

//           

// EXPANDED CLASSES

int main(int argc, char* argv[]) {
	cout << "Advanced SpaceTime Simulation Software starting up ...\n";

	cout << "ASTER loaded.\n";

	while (true) {
		cout << " > ";

		char inp[256];
		char cmd[256];
		for (char i = 0; i < 100; i++) {
			cmd[i] = 0;
			inp[i] = 0;
		}
		
		cin.getline(inp, 100); 
		char separator = ' ';
		int i = 0;
		
		string s; 
		while (inp[i] != '\0') {
			if (inp[i] != separator) {
				s += inp[i]; 
			} else {
				cmd[i] = s;
				s.clear();
			}
			i++;
		}

		cout << cmd[0] << cmd[1] << cmd[2] << "\n";
	}
}