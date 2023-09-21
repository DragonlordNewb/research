#include <iostream>

using namespace std;

class Vector {
	private:
		float x;
		float y;
		float z;
	public:
		Vector(float _x, float _y, float _z) {
			x = _x;
			y = _y;
			z = _z;
		}

		Vector operator+(Vector const& obj) {
			xn = x + obj.x;
			yn = y + obj.y;
			zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator-(Vector const& obj) {
			xn = x + obj.x;
			yn = y + obj.y;
			zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}
};

int main() {
	cout << "Hello World";
}