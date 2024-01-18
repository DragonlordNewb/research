#include <iostream>
#include <cmath>
#include <sstream>

using namespace std;

namespace constants {

	const double c = 2.99792458e+8;
	const double c2 = c * c;
	const double G = 6.6743e-11;
	const double Qe = 1.602176634e-19;
	const double ke = 8.9875517923e+9;
	const double alpha = 0.0072973525693;
	const double h = 6.62607015e-34;
	const double mu0 = 2 * (alpha / (Qe * Qe)) * h / c;
	const double epsilon0 = 1 / (mu0 * c2);

};

class Vec3 {

	public:

		double x, y, z;

		Vec3() {
			x = 0;
			y = 0;
			z = 0;
		}

		Vec3(double x, double y, double z) : x(x), y(y), z(z) {}

		double abs() {
			return sqrt((x * x) + (y * y) + (z * z));
		}

		Vec3 operator+(const Vec3 other) {
			return Vec3(x + other.x, y + other.y, z + other.z);
		}

		Vec3 operator-(const Vec3 other) {
			return Vec3(x - other.x, y - other.y, z - other.z);
		}

		Vec3 operator*(const double factor) {
			return Vec3(x * factor, y * factor, z * factor);
		}

		Vec3 operator*(const Vec3 other) {
			return Vec3(x * other.x, y * other.y, z * other.z);
		}

		Vec3 operator/(const double factor) {
			return Vec3(x / factor, y / factor, z / factor);
		}

		Vec3 operator/(const Vec3 other) {
			return Vec3(x / other.x, y / other.y, z / other.z);
		}

		double dot(const Vec3 other) {
			return x * other.x + y * other.y + z * other.z;
		}

		Vec3 cross(const Vec3 other) {
			return Vec3(y * other.z - z * other.y, z * other.x - x * other.z, x * other.y - y * other.x);
		}

};

// Class Vec4 definition (similar to Vec3)
class Vec4 {

	public:

		double t, x, y, z;

		Vec4(double t, double x, double y, double z) : t(t), x(x), y(y), z(z) {}

		string repr() {
			stringstream ss;
			return ss.str();
		}

		double abs() {
			return sqrt((t * t) + (x * x) + (y * y) + (z * z));
		}

		Vec4 operator+(const Vec4 other) {
			return Vec4(t + other.t, x + other.x, y + other.y, z + other.z);
		}

		Vec4 operator-(const Vec4 other) {
			return Vec4(t - other.t, x - other.x, y - other.y, z - other.z);
		}

		Vec4 operator*(const double factor) {
			return Vec4(t * factor, x * factor, y * factor, z * factor);
		}

		Vec4 operator*(const Vec4 other) {
			return Vec4(t * other.t, x * other.x, y * other.y, z * other.z);
		}

		Vec4 operator/(const double factor) {
			return Vec4(t / factor, x / factor, y / factor, z / factor);
		}

		Vec4 operator/(const Vec4 other) {
			return Vec4(t / other.t, x / other.x, y / other.y, z / other.z);
		}

		// Other member functions similar to Vec3
};

class Particle {

	private:

		double experiencedTime;
		Vec3 experiencedSpace;

	public:

		double restMass;
		double charge;
		Vec3 location;
		Vec3 velocity;
		Vec3 rotation;
		Vec3 spin;

		Particle(double restMass_=1, double charge_=1) {
			restMass = restMass_;
			charge = charge_;

		}

		double gamma() {
			return 1 / (1 - (pow(velocity.abs(), 2) / constants::c2));
		}

};

class Spacetime;

class MetricComponent {

	public:

		MetricComponent() {}

		virtual double value(Spacetime* spacetime, Vec3 location, Vec4 displacement) = 0;

		double value(Vec3 location, Vec4 displacement) {
			return 0.0;
		}

};

class MetricTensor {

	private:

		MetricComponent* tensor[4][4];

		MetricTensor() {}

		MetricComponent get(int mu, int nu) {
			return *(tensor[nu][mu])
		}

};

class Spacetime {

	public:

		MetricTensor metric;

};

int main(int argc, char* argv[]) {
	string input;
	string command = argv[1];

	if (command == "ping") {
		cout << "pong" << endl;
	} else if (command == "echo") {
		cin >> input;
		cout << input << endl;
	}
}