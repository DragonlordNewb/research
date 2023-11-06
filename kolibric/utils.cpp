#pragma once

#include <cmath>
#include <iostream>
#include <sstream>

using namespace std;

class Vec3 {

	public:

		double x;
		double y;
		double z;

		Vec3(double _x, double _y, double _z) {
			x = _x;
			y = _y;
			z = _z;
		}

		Vec3(double v) {
			x = v;
			y = v;
			z = v;
		}

		Vec3() {
			x = 0;
			y = 0;
			z = 0;
		}

		Vec3 operator+(Vec3 v) const {
			return Vec3(x + v.x, y + v.y, z + v.z);
		}

		Vec3 operator-(Vec3 v) const {
			return Vec3(x - v.x, y - v.y, z - v.z);
		}

		Vec3 operator*(double k) const {
			return Vec3(x * k, y * k, z * k);
		}

		Vec3 operator/(double k) const {
			return Vec3(x / k, y / k, z / k);
		}

		double magnitude() const {
      		return std::sqrt(x * x + y * y + z * z);
    	}

    	double dot(Vec3 v) const {
        	return x * v.x + y * v.y + z * v.z;
    	}

		Vec3 cross(Vec3 v) const {
        	return Vec3(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x);
    	}

		string repr() {
			stringstream ss;
			ss << "<" << x << ", " << y << ", " << z << ">";
			return ss.str();
		}

};

class Vec4 {

	public:

		double t;
		double x;
		double y;
		double z;

		Vec4(double _t, double _x, double _y, double _z) {
			t = _t;
			x = _x;
			y = _y;
			z = _z;
		}

		Vec4(double v) {
			t = v;
			x = v;
			y = v;
			z = v;
		}

		Vec4() {
			t = 0;
			x = 0;
			y = 0;
			z = 0;
		}

		Vec4 operator+(Vec4 v) const {
			return Vec4(t + v.t, x + v.x, y + v.y, z + v.z);
		}

		Vec4 operator-(Vec4 v) const {
			return Vec4(t - v.t, x - v.x, y - v.y, z - v.z);
		}

		Vec4 operator*(double k) const {
			return Vec4(t * k, x * k, y * k, z * k);
		}

		Vec4 operator/(double k) const {
			return Vec4(t / k, x / k, y / k, z / k);
		}

		double magnitude() const {
      		return sqrt((t * t) + (x * x) + (y * y) + (z * z));
    	}

		string repr() {
			stringstream ss;
			ss << "<" << t << ", " << x << ", " << y << ", " << z << ">";
			return ss.str();
		}

};