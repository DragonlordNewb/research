#include <iostream>
#include <cmath>
#include <sstream>

using namespace std;

class Vec3 {

	public:

		double x, y, z;

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