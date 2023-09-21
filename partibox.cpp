#include <iostream>

using namespace std;

// UTILITIES 

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
			float xn = x + obj.x;
			float yn = y + obj.y;
			float zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}

		Vector operator-(Vector const& obj) {
			float xn = x + obj.x;
			float yn = y + obj.y;
			float zn = z + obj.z; 
			return Vector(xn, yn, zn);
		}
};

int main(int argc, char* argv[]) {
	cout << "Hello World";
	cout << argv[0];
}