#pragma once

#include <iostream>
#include <cmath>

class Vec4 {

	public:

		double t, x, y, z;

		// Constructors
		Vec4() : t(0.0), x(0.0), y(0.0), z(0.0) {}
		Vec4(double t, double x, double y, double z) : t(t), x(x), y(y), z(z) {}

		// Copy constructor
		Vec4(const Vec4& other) : t(other.t), x(other.x), y(other.y), z(other.z) {}

		// Destructor
		~Vec4() {}

		// Assignment operator
		Vec4& operator=(const Vec4& other) {
			if (this != &other) {
				t = other.t;
				x = other.x;
				y = other.y;
				z = other.z;
			}
			return *this;
		}

		// Mathematical operations

		// Vector addition
		Vec4 operator+(const Vec4& other) const {
			return Vec4(t + other.t, x + other.x, y + other.y, z + other.z);
		}

		// Vector subtraction
		Vec4 operator-(const Vec4& other) const {
			return Vec4(t - other.t, x - other.x, y - other.y, z - other.z);
		}

		// Scalar multiplication
		Vec4 operator*(double scalar) const {
			return Vec4(t * scalar, x * scalar, y * scalar, z * scalar);
		}

		// Scalar division
		Vec4 operator/(double scalar) const {
			if (scalar != 0.0) {
				double invScalar = 1.0 / scalar;
				return Vec4(t * invScalar, x * invScalar, y * invScalar, z * invScalar);
			} else {
				std::cerr << "Error: Division by zero!" << std::endl;
				return Vec4();
			}
		}

		// Output stream operator
		friend std::ostream& operator<<(std::ostream& os, const Vec4& v) {
			os << "(" << v.t << ", " << v.x << ", " << v.y << ", " << v.z << ")";
			return os;
		}

};