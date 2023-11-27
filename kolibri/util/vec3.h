#pragma once

#include <iostream>
#include <cmath>

class Vec3 {

	public:

		double x, y, z;

		// Constructors
		Vec3() : x(0.0), y(0.0), z(0.0) {}
		Vec3(double x, double y, double z) : x(x), y(y), z(z) {}

		// Copy constructor
		Vec3(const Vec3& other) : x(other.x), y(other.y), z(other.z) {}

		// Destructor
		~Vec3() {}

		// Assignment operator
		Vec3& operator=(const Vec3& other) {
			if (this != &other) {
				x = other.x;
				y = other.y;
				z = other.z;
			}
			return *this;
		}

		// Mathematical operations

		// Vector addition
		Vec3 operator+(const Vec3& other) const {
			return Vec3(x + other.x, y + other.y, z + other.z);
		}

		// Vector subtraction
		Vec3 operator-(const Vec3& other) const {
			return Vec3(x - other.x, y - other.y, z - other.z);
		}

		// Scalar multiplication
		Vec3 operator*(double scalar) const {
			return Vec3(x * scalar, y * scalar, z * scalar);
		}

		// Scalar division
		Vec3 operator/(double scalar) const {
			if (scalar != 0.0) {
				double invScalar = 1.0 / scalar;
				return Vec3(x * invScalar, y * invScalar, z * invScalar);
			} else {
				std::cerr << "Error: Division by zero!" << std::endl;
				return Vec3();
			}
		}

		// Dot product
		double dot(const Vec3& other) const {
			return x * other.x + y * other.y + z * other.z;
		}

		// Cross product
		Vec3 cross(const Vec3& other) const {
			return Vec3(y * other.z - z * other.y, z * other.x - x * other.z, x * other.y - y * other.x);
		}

		// Magnitude (length) of the vector
		double length() const {
			return std::sqrt((x * x) + (y * y) + (z * z));
		}

		double length2() const {
			return (x * x) + (y * y) + (z * z);
		}

		// Normalize the vector (make it a unit vector)
		Vec3 normalize() const {
			double len = length();
			if (len != 0.0) {
				double invLen = 1.0 / len;
				return *this * invLen;
			} else {
				std::cerr << "Error: Normalizing a zero-length vector!" << std::endl;
				return Vec3();
			}
		}

		// Output stream operator
		friend std::ostream& operator<<(std::ostream& os, const Vec3& v) {
			os << "Vec3(" << v.x << ", " << v.y << ", " << v.z << ")";
			return os;
		}
		
};